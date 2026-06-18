"""
全局 conftest - 环境加载 + API fixtures
"""

import os
import yaml
import pytest
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def _load_env_config() -> dict:
    """加载环境配置，优先级：环境变量 > .env > env.yaml"""
    env_name = os.getenv("CB_ENV", "local")
    config_path = Path(__file__).parent / "config" / "env.yaml"

    with open(config_path) as f:
        all_configs = yaml.safe_load(f)

    config = all_configs["environments"][env_name].copy()

    # 环境变量覆盖
    overrides = {
        "tos_host": os.getenv("CB_TOS_HOST"),
        "tos_port": int(os.getenv("CB_TOS_PORT", 0)) or None,
        "username": os.getenv("CB_USERNAME"),
        "password": os.getenv("CB_PASSWORD"),
    }
    for k, v in overrides.items():
        if v is not None:
            config[k] = v

    return config


@pytest.fixture(scope="session")
def env_config():
    """环境配置"""
    return _load_env_config()


@pytest.fixture(scope="session")
def tos_client(env_config):
    """TOS HTTP 客户端（session级，全局共享）"""
    from client.base import TOSHttpClient
    client = TOSHttpClient(env_config)
    yield client
    client.close()


@pytest.fixture(scope="session")
def win_api(tos_client):
    """PC/Server API"""
    from client.win_api import WinAPI
    return WinAPI(tos_client)


@pytest.fixture(scope="session")
def file_api(tos_client):
    """FileServer API"""
    from client.file_api import FileAPI
    return FileAPI(tos_client)


@pytest.fixture(scope="session")
def vmware_api(tos_client):
    """VMware API"""
    from client.vmware_api import VMwareAPI
    return VMwareAPI(tos_client)


@pytest.fixture(scope="session")
def hyperv_api(tos_client):
    """Hyper-V API"""
    from client.hyperv_api import HyperVAPI
    return HyperVAPI(tos_client)


@pytest.fixture(scope="session")
def tos_api(tos_client):
    """TOS System API"""
    from client.tos_api import TOSAPI
    return TOSAPI(tos_client)


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """配置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


@pytest.fixture(autouse=True)
def log_test_name(request):
    """每条用例打印名称"""
    logging.info(f"▶ {request.node.nodeid}")
