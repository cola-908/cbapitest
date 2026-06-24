"""
TOSHttpClient - TOS认证 + 自动代理路由

核心能力:
1. 自动登录获取 Cookie + CSRF Token
2. 根据 API 路径前缀自动选择 proxy/proxy2 代理
3. 会话保持 + 请求重试
4. 统一响应封装
"""

import time
import logging
from typing import Any, Optional
from dataclasses import dataclass, field

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("cb-api-test")

# ── 代理路由规则 ──────────────────────────────────────
PROXY_RULES = {
    "/win": {
        "prefix": "/v2/proxy/CentralizedBackup",
        "strip": "/win",
    },
    "/file": {
        "prefix": "/v2/proxy2/CentralizedBackup",
        "strip": "/file",
    },
    "/VMware": {
        "prefix": "/v2/proxy2/CentralizedBackup",
        "strip": "/VMware",
    },
    "/hyperV": {
        "prefix": "/v2/proxy2/CentralizedBackup/58200",
        "strip": "/hyperV",
    },
}


@dataclass
class APIResponse:
    """统一响应封装"""
    status_code: int
    data: Any = None
    message: str = ""
    code: bool = True
    raw: Optional[dict] = None
    elapsed: float = 0.0

    @property
    def ok(self) -> bool:
        return self.status_code == 200 and self.code is True


class TOSHttpClient:
    """TOS认证 HTTP 客户端"""

    def __init__(self, config: dict):
        self.config = config
        self.session = requests.Session()

        scheme = "https" if config.get("use_https") else "http"
        self.base_url = f"{scheme}://{config['tos_host']}:{config['tos_port']}"
        self.timeout = config.get("timeout", 30)

        # 配置重试
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # 自动登录
        self._csrf_token: str = ""
        self._login(config["username"], config["password"])

    # ── 认证 ──────────────────────────────────────
    def _login(self, username: str, password: str) -> None:
        """登录 TOS，获取 Cookie 和 CSRF Token"""
        # Step 1: Get CSRF token and RSA public key
        # Note: /v2/system/info may return 404 but still provides CSRF + RSA headers
        info_resp = self.session.get(
            f"{self.base_url}/v2/system/info",
            timeout=self.timeout,
        )
        # Don't raise_for_status here - TOS may return 404 with valid headers

        # Step 2: RSA encrypt the password
        import base64
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5

        rsa_token = info_resp.headers.get("X-Rsa-Token", "")
        if not rsa_token:
            raise AuthenticationError("No RSA token from TOS")

        rsa_key = RSA.import_key(base64.b64decode(rsa_token))
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(password.encode())
        encrypted_b64 = base64.b64encode(encrypted).decode()

        # Step 3: Login with encrypted password
        # Extract CSRF token from cookies and set it in headers
        csrf_token = self.session.cookies.get("X-Csrf-Token", "")
        if csrf_token:
            self.session.headers.update({"X-Csrf-Token": csrf_token})

        resp = self.session.post(
            f"{self.base_url}/v2/login",
            json={"username": username, "password": encrypted_b64},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        body = resp.json()

        if not body.get("code", False):
            raise AuthenticationError(f"Login failed: {body.get('msg', 'unknown')}")

        # Update CSRF token from cookies after login
        self._csrf_token = self.session.cookies.get("X-Csrf-Token", csrf_token)
        if self._csrf_token:
            self.session.headers.update({"X-Csrf-Token": self._csrf_token})

        self.session.headers.update({"X-Csrf-Token": self._csrf_token})
        logger.info(f"Logged in as {username}, CSRF={self._csrf_token[:8]}...")

    # ── 代理路由 ──────────────────────────────────
    def _build_url(self, raw_path: str) -> str:
        """将前端 API 路径转换为 TOS 代理 URL"""
        for prefix, rule in PROXY_RULES.items():
            if raw_path.startswith(prefix):
                path = raw_path.replace(rule["strip"], "", 1)
                return f"{self.base_url}{rule['prefix']}{path}"
        # Paths not matching any module prefix route through CB proxy
        # e.g. /overview -> /v2/proxy/CentralizedBackup/overview
        if not raw_path.startswith("/v2/") and not raw_path.startswith("/CentralizedBackup"):
            return f"{self.base_url}/v2/proxy/CentralizedBackup{raw_path}"
        # Non-CB modules (like /v2/*) direct
        return f"{self.base_url}{raw_path}"

    # ── 核心请求方法 ──────────────────────────────
    def get(self, path: str, params: Optional[dict] = None, **kwargs) -> APIResponse:
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: Optional[dict] = None, **kwargs) -> APIResponse:
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Optional[dict] = None, **kwargs) -> APIResponse:
        return self._request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, json: Optional[dict] = None, **kwargs) -> APIResponse:
        return self._request("DELETE", path, json=json, **kwargs)

    def _request(self, method: str, path: str, **kwargs) -> APIResponse:
        url = self._build_url(path)
        kwargs.setdefault("timeout", self.timeout)

        start = time.time()
        resp = self.session.request(method, url, **kwargs)
        elapsed = time.time() - start

        # 解析响应
        try:
            body = resp.json()
        except Exception:
            body = {}

        api_resp = APIResponse(
            status_code=resp.status_code,
            data=body.get("data"),
            message=body.get("msg", ""),
            code=body.get("code", False),
            raw=body,
            elapsed=elapsed,
        )

        logger.debug(f"{method} {path} → {resp.status_code} ({elapsed:.3f}s)")
        return api_resp

    # ── 便捷方法 ──────────────────────────────────
    def health_check(self) -> dict:
        """检查各后端服务状态"""
        results = {}
        for name, path in [
            ("PC/Server", "/win/overview"),
            ("FileServer", "/file/FileServer/overview"),
            ("VMware", "/VMware/vmware/overview"),
            ("Hyper-V", "/hyperV/api/overview"),
        ]:
            resp = self.get(path)
            results[name] = resp.ok
        return results

    def close(self):
        self.session.close()


class AuthenticationError(Exception):
    """认证失败"""
    pass
