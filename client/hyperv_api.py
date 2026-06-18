"""
Hyper-V API - 37个接口

按业务实体分组:
- 设备管理 (12)
- 任务管理 (11)
- 还原任务 (8)
- Portal浏览 (4)
- 概览 (1)
- 下载 (1)
"""

from typing import Any, Optional
from client.base import TOSHttpClient, APIResponse


class HyperVAPI:
    """Hyper-V 虚拟机备份还原 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ── 设备管理 (12) ─────────────────────────────────
    def list_devices(self, is_update_online: Optional[bool] = None) -> APIResponse:
        params = {"is_update_online": is_update_online} if is_update_online is not None else None
        return self.client.get("/hyperV/api/devices", params=params)

    def get_device(self, device_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}")

    def add_device(self, data: dict) -> APIResponse:
        return self.client.post("/hyperV/api/devices/add", json=data)

    def edit_device(self, device_id: str, data: dict) -> APIResponse:
        return self.client.put(f"/hyperV/api/devices/{device_id}/edit", json=data)

    def delete_device(self, device_id: str) -> APIResponse:
        return self.client.delete(f"/hyperV/api/devices/{device_id}/delete")

    def get_device_state(self, device_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/get_state")

    def get_default_cfg(self, device_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/default_cfg")

    def get_vm_list(self, device_id: str, refresh: bool = True) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/get_vm", params={"refresh": refresh})

    def list_device_vms(self, device_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/vm")

    def get_vm_default_dirs(self, device_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/vm_default_dirs")

    def list_device_drv_dir(self, device_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/drv/dir")

    def list_device_drv_letter(self, device_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/drv/letter")

    def list_dir(self, device_id: str, data: dict) -> APIResponse:
        return self.client.post(f"/hyperV/api/devices/{device_id}/list_dir", json=data)

    def list_device_tasks(self, device_id: str, vm_name: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/devices/{device_id}/{vm_name}/tasks")

    # ── 任务管理 (11) ─────────────────────────────────
    def list_tasks(self) -> APIResponse:
        return self.client.get("/hyperV/api/tasks")

    def get_task(self, task_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/tasks/{task_id}")

    def get_task_detail(self, task_id: str, detail_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/tasks/{task_id}/{detail_id}")

    def add_task(self, data: dict) -> APIResponse:
        return self.client.post("/hyperV/api/tasks/add", json=data)

    def edit_task(self, task_id: str, data: dict) -> APIResponse:
        return self.client.put(f"/hyperV/api/tasks/{task_id}/edit", json=data)

    def exec_task(self, task_id: str) -> APIResponse:
        return self.client.put(f"/hyperV/api/tasks/{task_id}/exec")

    def stop_task(self, task_id: str) -> APIResponse:
        return self.client.put(f"/hyperV/api/tasks/{task_id}/stop")

    def delete_task(self, task_id: str) -> APIResponse:
        return self.client.delete(f"/hyperV/api/tasks/{task_id}/delete")

    def delete_task_version(self, task_id: str, ver_id: str) -> APIResponse:
        return self.client.delete(f"/hyperV/api/tasks/{task_id}/{ver_id}/delete")

    def get_task_version_detail(self, task_id: str, ver_id: str, sub_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/tasks/{task_id}/{ver_id}/{sub_id}")

    def delete_task_sub(self, task_id: str, ver_id: str, sub_id: str) -> APIResponse:
        return self.client.delete(f"/hyperV/api/tasks/{task_id}/{ver_id}/{sub_id}")

    # ── 还原任务 (8) ──────────────────────────────────
    def list_restore_tasks(self) -> APIResponse:
        return self.client.get("/hyperV/api/tasks/restoretask")

    def get_restore_task(self, task_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/tasks/restoretask/{task_id}")

    def list_restores(self) -> APIResponse:
        return self.client.get("/hyperV/api/tasks/restore")

    def get_restore(self, restore_id: str) -> APIResponse:
        return self.client.get(f"/hyperV/api/tasks/restore/{restore_id}")

    def add_restore(self, data: dict) -> APIResponse:
        return self.client.post("/hyperV/api/tasks/restore/add", json=data)

    def exec_restore(self, restore_id: str) -> APIResponse:
        return self.client.put(f"/hyperV/api/tasks/restore/{restore_id}/exec")

    def stop_restore(self, restore_id: str) -> APIResponse:
        return self.client.put(f"/hyperV/api/tasks/restore/{restore_id}/stop")

    def delete_restore(self, restore_id: str) -> APIResponse:
        return self.client.delete(f"/hyperV/api/tasks/restore/{restore_id}/delete")

    # ── Portal浏览 (4) ────────────────────────────────
    def browse_part(self, data: dict) -> APIResponse:
        return self.client.post("/hyperV/api/portal/browse_part", json=data)

    def disk_parts(self) -> APIResponse:
        return self.client.get("/hyperV/api/portal/disk/parts")

    def disk_view_browse(self, data: dict) -> APIResponse:
        return self.client.post("/hyperV/api/portal/disk/view/browse", json=data)

    def get_disk_parts(self, file_path: str) -> APIResponse:
        return self.client.get("/hyperV/api/portal/get_disk_parts", params={"file": file_path})

    # ── 概览 (1) ──────────────────────────────────────
    def overview(self) -> APIResponse:
        return self.client.get("/hyperV/api/overview")

    # ── 下载 (1) ──────────────────────────────────────
    def download_boot_image(self) -> APIResponse:
        return self.client.get("/databack/Centralized Backup Boot Image Creation Wizard.zip")
