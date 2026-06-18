"""
TOS System API - 10个接口

用于CB应用辅助操作：文件管理、存储卷、语言、版本等
"""

from client.base import TOSHttpClient, APIResponse


class TOSAPI:
    """TOS 系统级 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ── 语言 ──────────────────────────────────────────
    def get_lang(self) -> APIResponse:
        """GET /v2/lang/CentralizedBackup"""
        return self.client.get("/v2/lang/CentralizedBackup")

    # ── 应用版本 ───────────────────────────────────────
    def get_app_version(self) -> APIResponse:
        """GET /v2/app/version/CentralizedBackup"""
        return self.client.get("/v2/app/version/CentralizedBackup")

    def get_version_generic(self, app_id: str) -> APIResponse:
        """GET /v2/app/version/{app_id}"""
        return self.client.get(f"/v2/app/version/{app_id}")

    # ── 桌面显示 ───────────────────────────────────────
    def get_desktop_display(self) -> APIResponse:
        """GET /v2/person/desktopDisplay"""
        return self.client.get("/v2/person/desktopDisplay")

    # ── 文件管理 ───────────────────────────────────────
    def create_folder(self, path: str) -> APIResponse:
        """POST /v2/fileManage/CreateFolder"""
        return self.client.post("/v2/fileManage/CreateFolder", json={"path": path})

    def get_folder_info(self, path: str) -> APIResponse:
        """GET /v2/fileManage/folderInfo?path={}"""
        return self.client.get("/v2/fileManage/folderInfo", params={"path": path})

    def get_home_list(self) -> APIResponse:
        """GET /v2/fileManage/homeList"""
        return self.client.get("/v2/fileManage/homeList")

    def list_folders(self) -> APIResponse:
        """GET /v2/folder/list"""
        return self.client.get("/v2/folder/list")

    # ── 存储卷 ────────────────────────────────────────
    def list_volumes(self) -> APIResponse:
        """GET /v2/storage/list/volume"""
        return self.client.get("/v2/storage/list/volume")

    # ── 系统恢复 ──────────────────────────────────────
    def reinstall_system(self, data: dict) -> APIResponse:
        """POST /v2/updaterestore/reinstallSystem"""
        return self.client.post("/v2/updaterestore/reinstallSystem", json=data)

    # ── 客户端下载 ────────────────────────────────────
    def download_client_package(self) -> APIResponse:
        """GET /CentralizedBackup/clientPackage"""
        return self.client.get("/CentralizedBackup/clientPackage")
