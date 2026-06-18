"""
FileServer API - 33个接口

按业务实体分组:
- 设备管理 (4)
- 登录管理 (4)
- 备份任务 (9)
- 版本管理 (4)
- 还原任务 (6)
- 其他 (2)
"""

from typing import Any, Optional
from client.base import TOSHttpClient, APIResponse


class FileAPI:
    """FileServer 文件备份还原 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ── 设备管理 (4) ──────────────────────────────────
    def list_devices(self) -> APIResponse:
        """GET /file/FileServer/device"""
        return self.client.get("/file/FileServer/device")

    def get_device(self, device_id: int) -> APIResponse:
        """GET /file/FileServer/device/{device_id}"""
        return self.client.get(f"/file/FileServer/device/{device_id}")

    def add_device(self, data: dict) -> APIResponse:
        """POST /file/FileServer/device"""
        return self.client.post("/file/FileServer/device", json=data)

    def delete_device(self, device_id: int) -> APIResponse:
        """DELETE /file/FileServer/device/{device_id}"""
        return self.client.delete(f"/file/FileServer/device/{device_id}")

    def read_dir(self, path: str) -> APIResponse:
        """POST /file/FileServer/device/readDir"""
        return self.client.post("/file/FileServer/device/readDir", json={"path": path})

    # ── 登录管理 (4) ──────────────────────────────────
    def list_logins(self) -> APIResponse:
        """GET /file/FileServer/login"""
        return self.client.get("/file/FileServer/login")

    def add_login(self, data: dict) -> APIResponse:
        """POST /file/FileServer/login/"""
        return self.client.post("/file/FileServer/login/", json=data)

    def edit_login(self, login_id: int, data: dict) -> APIResponse:
        """PUT /file/FileServer/login/{login_id}/edit"""
        return self.client.put(f"/file/FileServer/login/{login_id}/edit", json=data)

    def get_login_state(self, login_id: int) -> APIResponse:
        """GET /file/FileServer/login_state/{login_id}"""
        return self.client.get(f"/file/FileServer/login_state/{login_id}")

    # ── 备份任务 (9) ──────────────────────────────────
    def list_backup_tasks(self) -> APIResponse:
        """GET /file/FileServer/backup_task"""
        return self.client.get("/file/FileServer/backup_task")

    def get_backup_task(self, task_id: int) -> APIResponse:
        """GET /file/FileServer/backup_task/{task_id}"""
        return self.client.get(f"/file/FileServer/backup_task/{task_id}")

    def add_backup_task(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task"""
        return self.client.post("/file/FileServer/backup_task", json=data)

    def edit_backup_task(self, task_id: int, data: dict) -> APIResponse:
        """PUT /file/FileServer/task/{task_id}/edit"""
        return self.client.put(f"/file/FileServer/task/{task_id}/edit", json=data)

    def start_backup_task(self, task_id: int) -> APIResponse:
        """POST /file/FileServer/task/{task_id}/start"""
        return self.client.post(f"/file/FileServer/task/{task_id}/start")

    def stop_backup_task(self, task_id: int) -> APIResponse:
        """POST /file/FileServer/task/{task_id}/stop"""
        return self.client.post(f"/file/FileServer/task/{task_id}/stop")

    def start_backup(self, task_id: int) -> APIResponse:
        """POST /file/FileServer/backup_task/start"""
        return self.client.post(f"/file/FileServer/backup_task/start", json={"id": task_id})

    def stop_backup(self, task_id: int) -> APIResponse:
        """POST /file/FileServer/backup_task/stop"""
        return self.client.post(f"/file/FileServer/backup_task/stop", json={"id": task_id})

    def import_backup(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/import"""
        return self.client.post("/file/FileServer/backup_task/import", json=data)

    # ── 版本管理 (4) ──────────────────────────────────
    def list_versions(self, task_id: int) -> APIResponse:
        """GET /file/FileServer/backup_task/versions/{task_id}"""
        return self.client.get(f"/file/FileServer/backup_task/versions/{task_id}")

    def get_version(self, ver_id: int) -> APIResponse:
        """GET /file/FileServer/version/{ver_id}"""
        return self.client.get(f"/file/FileServer/version/{ver_id}")

    def delete_version(self, ver_id: int) -> APIResponse:
        """POST /file/FileServer/version/delete"""
        return self.client.post("/file/FileServer/version/delete", json={"id": ver_id})

    def set_version_locked(self, ver_id: int, locked: bool) -> APIResponse:
        """POST /file/FileServer/version/set_version_locked"""
        return self.client.post(
            "/file/FileServer/version/set_version_locked",
            json={"id": ver_id, "locked": locked},
        )

    def delete_backup_version(self, ver_id: int) -> APIResponse:
        """POST /file/FileServer/backup_task/versions/delete"""
        return self.client.post("/file/FileServer/backup_task/versions/delete", json={"id": ver_id})

    def lock_backup_version(self, ver_id: int, locked: bool) -> APIResponse:
        """POST /file/FileServer/backup_task/versions/lock"""
        return self.client.post(
            "/file/FileServer/backup_task/versions/lock",
            json={"id": ver_id, "locked": locked},
        )

    # ── 还原任务 (6) ──────────────────────────────────
    def list_restore_tasks(self) -> APIResponse:
        """GET /file/FileServer/restore_task"""
        return self.client.get("/file/FileServer/restore_task")

    def get_restore_task(self, task_id: int) -> APIResponse:
        """GET /file/FileServer/restore_task/{task_id}"""
        return self.client.get(f"/file/FileServer/restore_task/{task_id}")

    def list_restores(self) -> APIResponse:
        """GET /file/FileServer/restore"""
        return self.client.get("/file/FileServer/restore")

    def get_restore(self, restore_id: int) -> APIResponse:
        """GET /file/FileServer/restore/{restore_id}"""
        return self.client.get(f"/file/FileServer/restore/{restore_id}")

    def start_restore(self, restore_id: int) -> APIResponse:
        """POST /file/FileServer/restore/{restore_id}/start"""
        return self.client.post(f"/file/FileServer/restore/{restore_id}/start")

    def stop_restore(self, restore_id: int) -> APIResponse:
        """POST /file/FileServer/restore/{restore_id}/stop"""
        return self.client.post(f"/file/FileServer/restore/{restore_id}/stop")

    def start_restore_task(self, task_id: int) -> APIResponse:
        """POST /file/FileServer/restore_task/{task_id}/start"""
        return self.client.post(f"/file/FileServer/restore_task/{task_id}/start")

    def stop_restore_task(self, task_id: int) -> APIResponse:
        """POST /file/FileServer/restore_task/{task_id}/stop"""
        return self.client.post(f"/file/FileServer/restore_task/{task_id}/stop")

    # ── 其他 (2) ───────────────────────────────────────
    def list_tasks_legacy(self) -> APIResponse:
        """GET /file/FileServer/task"""
        return self.client.get("/file/FileServer/task")

    def get_smb_info(self) -> APIResponse:
        """GET /fileServer/SMB"""
        return self.client.get("/fileServer/SMB")

    # ── 概览 (1) ──────────────────────────────────────
    def overview(self) -> APIResponse:
        """GET /file/FileServer/overview"""
        return self.client.get("/file/FileServer/overview")
