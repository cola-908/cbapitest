"""
测试数据清理工具 - fixture teardown 时自动清理测试产生的资源
"""

import logging
from typing import Optional

logger = logging.getLogger("cb-api-test")


class ResourceTracker:
    """跟踪测试中创建的资源，teardown 时自动清理"""

    def __init__(self):
        self._resources: list[dict] = []  # [{"type": "win_device", "id": "xxx"}, ...]

    def add(self, resource_type: str, resource_id: str):
        self._resources.append({"type": resource_type, "id": resource_id})

    def cleanup_all(self, apis: dict):
        """按逆序清理所有已注册资源"""
        for res in reversed(self._resources):
            rtype, rid = res["type"], res["id"]
            try:
                if rtype == "win_device":
                    apis["win"].delete_device(rid)
                elif rtype == "file_device":
                    apis["file"].delete_device(int(rid))
                elif rtype == "vmware_device":
                    apis["vmware"].delete_device(int(rid))
                elif rtype == "hyperv_device":
                    apis["hyperv"].delete_device(rid)
                elif rtype == "win_task":
                    apis["win"].batch_delete_tasks([int(rid)])
                elif rtype == "file_task":
                    pass  # file task cleanup via device
                elif rtype == "vmware_task":
                    pass
                elif rtype == "hyperv_task":
                    apis["hyperv"].delete_task(rid)
                logger.info(f"Cleaned up {rtype} id={rid}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {rtype} id={rid}: {e}")

        self._resources.clear()


# ── Fixture ──────────────────────────────────────

import pytest


@pytest.fixture
def tracker():
    """资源跟踪器"""
    t = ResourceTracker()
    yield t
    # teardown 时由用例自行调用 cleanup_all
