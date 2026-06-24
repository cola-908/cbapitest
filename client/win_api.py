"""
PC/Server (Win) API - 覆盖21个测试用例

代理路径前缀 /win → /v2/proxy/CentralizedBackup

用例覆盖:
- CB-001, CB-001b: 查询设备(desktop/server)
- CB-002: 删除设备
- CB-003, CB-003b: 查询任务(desktop/server)
- CB-004: 导入备份数据
- CB-005: 创建整台设备备份任务
- CB-006: 执行备份
- CB-007: 批量取消任务
- CB-008: 删除任务
- CB-009: 批量编辑任务
- CB-017: Portal目录浏览
- CB-018: 概览
- CB-105: 编辑设备
- CB-106: 获取卷信息
- CB-107: 创建仅系统备份任务
- CB-108: 创建自定义卷备份任务
- CB-109: 获取任务版本
- CB-110: 任务版本上锁
- CB-111: 任务版本解锁
- CB-112: 删除任务版本
"""

from typing import Any, Optional
from client.base import TOSHttpClient, APIResponse


class WinAPI:
    """PC/Server 备份还原 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ── 设备管理 ──────────────────────────────────────
    def list_devices(self, device_type: Optional[str] = None) -> APIResponse:
        """GET /win/devices?type={desktop|server}
        覆盖: CB-001, CB-001b
        """
        params = {"type": device_type} if device_type else None
        return self.client.get("/win/devices", params=params)

    def get_device(self, device_id: str) -> APIResponse:
        """GET /win/devices?id={device_id}"""
        return self.client.get("/win/devices", params={"id": device_id})

    def delete_device(self, device_id: str) -> APIResponse:
        """DELETE /win/devices/{device_id}
        覆盖: CB-002
        """
        return self.client.delete(f"/win/devices/{device_id}")

    def batch_delete_devices(self, device_ids: list[str]) -> APIResponse:
        """POST /win/batch/devices/delete"""
        return self.client.post("/win/batch/devices/delete", json={"ids": device_ids})

    def edit_device(self, device_id: str, data: dict) -> APIResponse:
        """POST /win/devices/{device_id}
        覆盖: CB-105
        """
        return self.client.post(f"/win/devices/{device_id}", json=data)

    def get_device_volumes(self, device_id: str) -> APIResponse:
        """GET /win/devices/{device_id}/volumes
        覆盖: CB-106
        """
        return self.client.get(f"/win/devices/{device_id}/volumes")

    def get_device_tasks_summary(self, device_id: str) -> APIResponse:
        """GET /win/devices/{device_id}/tasks"""
        return self.client.get(f"/win/devices/{device_id}/tasks")

    def get_device_task_versions(self, device_id: str, task_id: str | int) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}/version
        覆盖: CB-006
        """
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}/version")

    def get_device_task_detail(self, device_id: str, task_id: str | int) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}"""
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}")

    # ── 任务管理 ──────────────────────────────────────
    def list_tasks(self, task_type: Optional[str] = None) -> APIResponse:
        """GET /win/tasks?type={desktop|server}
        覆盖: CB-003, CB-003b
        """
        params = {"type": task_type} if task_type else None
        return self.client.get("/win/tasks", params=params)

    def relink_task(self, data: Optional[dict] = None) -> APIResponse:
        """POST /win/tasks/relink
        覆盖: CB-004
        """
        return self.client.post("/win/tasks/relink", json=data)

    def relink_task_with_type(self, task_type: str) -> APIResponse:
        """POST /win/tasks/relink?type={desktop|server}"""
        return self.client.post("/win/tasks/relink", params={"type": task_type})

    # ── 创建备份任务（三个策略: 全设备/仅系统/自定义卷）──
    def create_backup_task_full(self, device_id: str, data: dict) -> APIResponse:
        """POST /win/devices/{device_id}/task  — 整台设备备份
        覆盖: CB-005
        """
        return self.client.post(f"/win/devices/{device_id}/task", json=data)

    def create_backup_task_system(self, device_id: str, data: dict) -> APIResponse:
        """POST /win/devices/{device_id}/task  — 仅系统备份
        覆盖: CB-107
        """
        return self.client.post(f"/win/devices/{device_id}/task", json=data)

    def create_backup_task_custom(self, device_id: str, data: dict) -> APIResponse:
        """POST /win/devices/{device_id}/task  — 自定义卷备份
        覆盖: CB-108
        """
        return self.client.post(f"/win/devices/{device_id}/task", json=data)

    # 通用创建方法（所有三个策略）
    def create_backup_task(self, device_id: str, data: dict) -> APIResponse:
        """POST /win/devices/{device_id}/task
        覆盖: CB-005, CB-107, CB-108
        """
        return self.client.post(f"/win/devices/{device_id}/task", json=data)

    # ── 版本管理 ──────────────────────────────────────
    def list_versions(self, device_id: str, task_id: str | int) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}/versions
        覆盖: CB-109
        """
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}/versions")

    def lock_task_version(
        self, device_id: str, task_id: str | int, version_id: str, data: Optional[dict] = None
    ) -> APIResponse:
        """POST /win/devices/{device_id}/tasks/{task_id}/versions/{version_id}
        覆盖: CB-110
        """
        return self.client.post(
            f"/win/devices/{device_id}/tasks/{task_id}/versions/{version_id}", json=data
        )

    def unlock_task_version(
        self, device_id: str, task_id: str | int, version_id: str, data: Optional[dict] = None
    ) -> APIResponse:
        """POST /win/devices/{device_id}/tasks/{task_id}/versions/{version_id}
        覆盖: CB-111
        """
        return self.client.post(
            f"/win/devices/{device_id}/tasks/{task_id}/versions/{version_id}", json=data
        )

    def delete_task_version(
        self, device_id: str, task_id: str | int, version_id: str, data: Optional[dict] = None
    ) -> APIResponse:
        """DELETE /win/devices/{device_id}/tasks/{task_id}/versions/{version_id}
        覆盖: CB-112
        """
        return self.client.delete(
            f"/win/devices/{device_id}/tasks/{task_id}/versions/{version_id}", json=data
        )

    # ── 任务删除 ──────────────────────────────────────
    def delete_task(self, device_id: str, task_id: str | int) -> APIResponse:
        """DELETE /win/devices/{device_id}/tasks/{task_id}
        覆盖: CB-008
        """
        return self.client.delete(f"/win/devices/{device_id}/tasks/{task_id}")

    # ── 批量操作 ──────────────────────────────────────
    def batch_exec_task(self, device_id: str, task_id: str | int, data: Optional[dict] = None) -> APIResponse:
        """POST /win/devices/{device_id}/tasks/{task_id}/version
        覆盖: CB-006
        """
        return self.client.post(
            f"/win/devices/{device_id}/tasks/{task_id}/version", json=data
        )

    def batch_cancel_tasks(self, data: dict) -> APIResponse:
        """POST /win/batch/tasks/cancel
        覆盖: CB-007
        """
        return self.client.post("/win/batch/tasks/cancel", json=data)

    def batch_delete_tasks(self, data: dict) -> APIResponse:
        """DELETE /win/batch/tasks/delete (通过 POST 模拟)
        注意: 根据用例 delete 转发为 POST /batch/tasks/delete
        """
        return self.client.post("/win/batch/tasks/delete", json=data)

    def batch_edit_task(self, device_id: str, task_id: str | int, data: dict) -> APIResponse:
        """POST /win/devices/{device_id}/tasks/{task_id}
        覆盖: CB-009
        """
        return self.client.post(f"/win/devices/{device_id}/tasks/{task_id}", json=data)

    def batch_add_tasks(self, data: dict) -> APIResponse:
        """POST /win/batch/tasks/add"""
        return self.client.post("/win/batch/tasks/add", json=data)

    def batch_exec_tasks(self, data: dict) -> APIResponse:
        """POST /win/batch/tasks/exec"""
        return self.client.post("/win/batch/tasks/exec", json=data)

    def batch_edit_tasks(self, data: dict) -> APIResponse:
        """POST /win/batch/tasks/edit"""
        return self.client.post("/win/batch/tasks/edit", json=data)

    # ── Portal 浏览 ──────────────────────────────────
    def portal_dir(self, path: Optional[str] = None) -> APIResponse:
        """GET /win/portal/dir
        覆盖: CB-017
        """
        params = {"path": path} if path else None
        return self.client.get("/win/portal/dir", params=params)

    def browse_image(self, file_id: str, sub_path: str = "") -> APIResponse:
        """GET /win/portal/browse_image"""
        return self.client.get(
            "/win/portal/browse_image",
            params={"file_id": file_id, "sub_path": sub_path},
        )

    def get_dev_dir_sub_dirs(self, device_uuid: str, path: str = "/") -> APIResponse:
        """GET /win/portal/get_dev_dir_sub_dirs"""
        return self.client.get(
            "/win/portal/get_dev_dir_sub_dirs",
            params={"device_uuid": device_uuid, "path": path},
        )

    # ── 概览 ──────────────────────────────────────────
    def overview(self) -> APIResponse:
        """GET /win/overview
        覆盖: CB-018
        """
        return self.client.get("/win/overview")

    # ── 客户端下载 ────────────────────────────────────
    def download_pc_client(self) -> APIResponse:
        """GET /win/pc/windows"""
        return self.client.get("/win/pc/windows")

    def download_server_client(self) -> APIResponse:
        """GET /win/server/windows"""
        return self.client.get("/win/server/windows")
