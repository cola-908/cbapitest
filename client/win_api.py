"""
PC/Server (Win) API - 39个接口

按业务实体分组:
- 设备管理 (8)
- 任务管理 (12)
- 版本管理 (6)
- 还原 (5)
- Portal浏览 (5)
- 概览 (1)
- 其他 (2)
"""

from typing import Any, Optional
from client.base import TOSHttpClient, APIResponse


class WinAPI:
    """PC/Server 备份还原 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ── 设备管理 (8) ──────────────────────────────────
    def list_devices(self, device_type: Optional[str] = None) -> APIResponse:
        """GET /win/devices?type={desktop|server}"""
        params = {"type": device_type} if device_type else None
        return self.client.get("/win/devices", params=params)

    def get_device(self, device_id: str) -> APIResponse:
        """GET /win/api/device/{device_id}"""
        return self.client.get(f"/win/api/device/{device_id}")

    def list_all_devices(self) -> APIResponse:
        """GET /win/api/device"""
        return self.client.get("/win/api/device")

    def delete_device(self, device_id: str) -> APIResponse:
        """DELETE /win/api/device/{device_id}"""
        return self.client.delete(f"/win/api/device/{device_id}")

    def batch_delete_devices(self, device_ids: list[str]) -> APIResponse:
        """POST /win/batch/devices/delete"""
        return self.client.post("/win/batch/devices/delete", json={"ids": device_ids})

    def get_device_volumes(self, device_id: str) -> APIResponse:
        """GET /win/api/device/{device_id}/volume"""
        return self.client.get(f"/win/api/device/{device_id}/volume")

    def upgrade_device(self, device_id: str) -> APIResponse:
        """PUT /win/devices/{device_id}/upgrade"""
        return self.client.put(f"/win/devices/{device_id}/upgrade")

    def get_device_tasks_summary(self, device_id: str) -> APIResponse:
        """GET /win/devices/{device_id}/task"""
        return self.client.get(f"/win/devices/{device_id}/task")

    # ── 任务管理 (12) ─────────────────────────────────
    def list_tasks(self, task_type: Optional[str] = None) -> APIResponse:
        """GET /win/tasks?type={desktop|server}"""
        params = {"type": task_type} if task_type else None
        return self.client.get("/win/tasks", params=params)

    def get_task(self, task_id: int) -> APIResponse:
        """GET /win/api/task/{task_id}"""
        return self.client.get(f"/win/api/task/{task_id}")

    def list_all_tasks(self) -> APIResponse:
        """GET /win/api/task"""
        return self.client.get("/win/api/task")

    def exec_task(self, task_id: int) -> APIResponse:
        """PUT /win/api/task/{task_id}/exec"""
        return self.client.put(f"/win/api/task/{task_id}/exec")

    def cancel_task(self, task_id: int) -> APIResponse:
        """PUT /win/api/task/{task_id}/cancel"""
        return self.client.put(f"/win/api/task/{task_id}/cancel")

    def get_task_verbose(self, task_id: int) -> APIResponse:
        """GET /win/api/task/{task_id}/verbose"""
        return self.client.get(f"/win/api/task/{task_id}/verbose")

    def edit_task(self, task_id: int, data: dict) -> APIResponse:
        """PUT /win/devices/{device_id}/tasks/{task_id}"""
        return self.client.put(f"/win/api/task/{task_id}", json=data)

    def relink_task(self, task_type: str) -> APIResponse:
        """GET /win/tasks/relink?type={desktop|server}"""
        return self.client.get("/win/tasks/relink", params={"type": task_type})

    def batch_add_tasks(self, tasks: list[dict]) -> APIResponse:
        """POST /win/batch/tasks/add"""
        return self.client.post("/win/batch/tasks/add", json={"tasks": tasks})

    def batch_exec_tasks(self, task_ids: list[int]) -> APIResponse:
        """POST /win/batch/tasks/exec"""
        return self.client.post("/win/batch/tasks/exec", json={"ids": task_ids})

    def batch_cancel_tasks(self, task_ids: list[int]) -> APIResponse:
        """POST /win/batch/tasks/cancel"""
        return self.client.post("/win/batch/tasks/cancel", json={"ids": task_ids})

    def batch_delete_tasks(self, task_ids: list[int]) -> APIResponse:
        """POST /win/batch/tasks/delete"""
        return self.client.post("/win/batch/tasks/delete", json={"ids": task_ids})

    def batch_edit_tasks(self, edits: list[dict]) -> APIResponse:
        """POST /win/batch/tasks/edit"""
        return self.client.post("/win/batch/tasks/edit", json={"edits": edits})

    # ── 版本管理 (6) ──────────────────────────────────
    def list_versions(self, device_id: str, task_id: int) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}/versions"""
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}/versions")

    def get_version(self, device_id: str, task_id: int, ver_id: str) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}/versions/{ver_id}"""
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}/versions/{ver_id}")

    def get_version_guide(self, device_id: str, task_id: int) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}/guide"""
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}/guide")

    def get_version_detail(self, device_id: str, task_id: int, ver_id: str) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}/version/{ver_id}"""
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}/version/{ver_id}")

    def lock_version(self, ver_id: str, locked: bool) -> APIResponse:
        """PUT version lock"""
        return self.client.put(f"/win/devices/0/tasks/0/versions/{ver_id}", json={"locked": locked})

    def get_disk_partitions(
        self, device_id: str, task_id: int, ver_id: str, disk_id: str, part_id: str
    ) -> APIResponse:
        """GET 最深层 /versions/{ver_id}/disks/{disk_id}/partitions/{part_id}"""
        return self.client.get(
            f"/win/devices/{device_id}/tasks/{task_id}/versions/{ver_id}/disks/{disk_id}/partitions/{part_id}"
        )

    # ── 还原 (5) ──────────────────────────────────────
    def list_restore_tasks(self) -> APIResponse:
        """GET /win/api/portal/get_res_task"""
        return self.client.get("/win/api/portal/get_res_task")

    def create_restore_task(self, data: dict) -> APIResponse:
        """POST /win/api/portal/create_res_task"""
        return self.client.post("/win/api/portal/create_res_task", json=data)

    def cancel_restore(self, res_id: int) -> APIResponse:
        """GET /win/api/portal/cancel_res?id={res_id}"""
        return self.client.get("/win/api/portal/cancel_res", params={"id": res_id})

    def delete_restore(self, res_id: int) -> APIResponse:
        """GET /win/api/portal/delete_res?id={res_id}"""
        return self.client.get("/win/api/portal/delete_res", params={"id": res_id})

    def restore(self, data: dict) -> APIResponse:
        """POST /win/api/portal/restore"""
        return self.client.post("/win/api/portal/restore", json=data)

    # ── Portal浏览 (5) ───────────────────────────────
    def browse_image(self, file_id: str, sub_path: str = "") -> APIResponse:
        """GET /win/api/portal/browse_image?file_id={}&sub_path={}"""
        return self.client.get(
            "/win/api/portal/browse_image",
            params={"file_id": file_id, "sub_path": sub_path},
        )

    def get_dev_dir_sub_dirs(self, device_uuid: str, path: str = "/") -> APIResponse:
        """GET /win/api/portal/get_dev_dir_sub_dirs?device_uuid={}&path={}"""
        return self.client.get(
            "/win/api/portal/get_dev_dir_sub_dirs",
            params={"device_uuid": device_uuid, "path": path},
        )

    def portal_dir(self, path: str = "/") -> APIResponse:
        """GET /win/portal/dir"""
        return self.client.get("/win/portal/dir", params={"path": path})

    def download_pc_client(self) -> APIResponse:
        """GET /pc/windows"""
        return self.client.get("/pc/windows")

    def download_server_client(self) -> APIResponse:
        """GET /server/windows"""
        return self.client.get("/server/windows")

    # ── 概览 (1) ──────────────────────────────────────
    def overview(self) -> APIResponse:
        """GET /win/overview"""
        return self.client.get("/win/overview")

    # ── 其他 (2) ──────────────────────────────────────
    def get_task_detail(self, device_id: str, task_id: int) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}"""
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}")

    def get_device_task_versions(self, device_id: str, task_id: int) -> APIResponse:
        """GET /win/devices/{device_id}/tasks/{task_id}/version"""
        return self.client.get(f"/win/devices/{device_id}/tasks/{task_id}/version")
