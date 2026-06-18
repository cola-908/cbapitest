"""
VMware API - 38个接口

按业务实体分组:
- 设备管理 (18)
- 任务管理 (11)
- 版本管理 (3)
- 还原任务 (5)
- 概览 (1)
"""

from typing import Any, Optional
from client.base import TOSHttpClient, APIResponse


class VMwareAPI:
    """VMware 虚拟机备份还原 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ── 设备管理 (18) ─────────────────────────────────
    def list_devices(self, update_status: Optional[bool] = None) -> APIResponse:
        """GET /VMware/vmware/device?update_status={true|false}"""
        params = {"update_status": update_status} if update_status is not None else None
        return self.client.get("/VMware/vmware/device", params=params)

    def get_device(self, device_id: int) -> APIResponse:
        """GET /VMware/vmware/device/{device_id}"""
        return self.client.get(f"/VMware/vmware/device/{device_id}")

    def add_device(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device"""
        return self.client.post("/VMware/vmware/device", json=data)

    def delete_device(self, device_id: int) -> APIResponse:
        """DELETE /VMware/vmware/device/{device_id}"""
        return self.client.delete(f"/VMware/vmware/device/{device_id}")

    def check_resource_enough(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/check_resource_is_enough"""
        return self.client.post("/VMware/vmware/device/check_resource_is_enough", json=data)

    def check_restore_support(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/check_restore_is_support"""
        return self.client.post("/VMware/vmware/device/check_restore_is_support", json=data)

    def check_vm_exist(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/check_vm_is_exist"""
        return self.client.post("/VMware/vmware/device/check_vm_is_exist", json=data)

    def get_device_status(self, device_id: int) -> APIResponse:
        """GET /VMware/vmware/device/{device_id}/device_status"""
        return self.client.get(f"/VMware/vmware/device/{device_id}/device_status")

    def get_linked_task(self, device_id: int) -> APIResponse:
        """GET /VMware/vmware/device/{device_id}/be_linked_task"""
        return self.client.get(f"/VMware/vmware/device/{device_id}/be_linked_task")

    def get_task_devices(self) -> APIResponse:
        """GET /VMware/vmware/get_task_devices/"""
        return self.client.get("/VMware/vmware/get_task_devices/")

    # ── 数据中心浏览系列 (9) ──────────────────────────
    def list_datacenters(self, device_id: int) -> APIResponse:
        """GET /VMware/vmware/device/datacenters/{device_id}"""
        return self.client.get(f"/VMware/vmware/device/datacenters/{device_id}")

    def list_datacenter_clusters(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_clusters"""
        return self.client.post("/VMware/vmware/device/datacenter_clusters", json=data)

    def list_datacenter_cluster_hosts(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_cluster_hosts"""
        return self.client.post("/VMware/vmware/device/datacenter_cluster_hosts", json=data)

    def list_datacenter_cluster_host_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_cluster_host_vms"""
        return self.client.post("/VMware/vmware/device/datacenter_cluster_host_vms", json=data)

    def list_datacenter_folders(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_folders"""
        return self.client.post("/VMware/vmware/device/datacenter_folders", json=data)

    def list_datacenter_folder_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_folder_vms"""
        return self.client.post("/VMware/vmware/device/datacenter_folder_vms", json=data)

    def list_datacenter_datastores(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_datastores"""
        return self.client.post("/VMware/vmware/device/datacenter_datastores", json=data)

    def list_datacenter_networks(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_networks"""
        return self.client.post("/VMware/vmware/device/datacenter_networks", json=data)

    def list_datacenter_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_vms"""
        return self.client.post("/VMware/vmware/device/datacenter_vms", json=data)

    def get_datacenter_vm(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_vm"""
        return self.client.post("/VMware/vmware/device/datacenter_vm", json=data)

    def vm_list(self, device_id: int) -> APIResponse:
        """GET /VMware/vm_list?id={device_id}"""
        return self.client.get("/VMware/vm_list", params={"id": device_id})

    # ── 任务管理 (11) ─────────────────────────────────
    def list_tasks(self) -> APIResponse:
        """GET /VMware/vmware/task"""
        return self.client.get("/VMware/vmware/task")

    def get_task(self, task_id: int) -> APIResponse:
        """GET /VMware/vmware/task/{task_id}"""
        return self.client.get(f"/VMware/vmware/task/{task_id}")

    def add_task(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task"""
        return self.client.post("/VMware/vmware/task", json=data)

    def import_task(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/import"""
        return self.client.post("/VMware/vmware/task/import", json=data)

    def start_task(self, task_id: int) -> APIResponse:
        """PUT /VMware/vmware/task/{task_id}/start"""
        return self.client.put(f"/VMware/vmware/task/{task_id}/start")

    def stop_task(self, task_id: int) -> APIResponse:
        """PUT /VMware/vmware/task/{task_id}/stop"""
        return self.client.put(f"/VMware/vmware/task/{task_id}/stop")

    def check_dest_folder(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/check_dest_folder"""
        return self.client.post("/VMware/vmware/task/check_dest_folder", json=data)

    def check_vm_service(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/check_vm_service"""
        return self.client.post("/VMware/vmware/task/check_vm_service", json=data)

    def get_disk_partitions(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/get_disk_partitions"""
        return self.client.post("/VMware/vmware/task/get_disk_partitions", json=data)

    def get_partition_system(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/get_partition_system"""
        return self.client.post("/VMware/vmware/task/get_partition_system", json=data)

    def get_task_ver_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/get_task_ver_vms"""
        return self.client.post("/VMware/vmware/task/get_task_ver_vms", json=data)

    # ── 版本管理 (3) ──────────────────────────────────
    def list_versions(self, task_id: int) -> APIResponse:
        """GET /VMware/vmware/task/version/{task_id}"""
        return self.client.get(f"/VMware/vmware/task/version/{task_id}")

    def get_version(self, ver_id: int) -> APIResponse:
        """GET /VMware/vmware/task/version (detail)"""
        return self.client.get("/VMware/vmware/task/version", params={"id": ver_id})

    def set_ver_locked(self, ver_id: int, locked: bool) -> APIResponse:
        """POST /VMware/vmware/task/version/set_ver_locked"""
        return self.client.post(
            "/VMware/vmware/task/version/set_ver_locked",
            json={"id": ver_id, "locked": locked},
        )

    # ── 还原任务 (5) ──────────────────────────────────
    def list_restore_tasks(self) -> APIResponse:
        """GET /VMware/vmware/restore_task"""
        return self.client.get("/VMware/vmware/restore_task")

    def get_restore_task(self, task_id: int) -> APIResponse:
        """GET /VMware/vmware/restore_task/{task_id}"""
        return self.client.get(f"/VMware/vmware/restore_task/{task_id}")

    def start_restore_task(self, task_id: int) -> APIResponse:
        """PUT /VMware/vmware/restore_task/{task_id}/start"""
        return self.client.put(f"/VMware/vmware/restore_task/{task_id}/start")

    def stop_restore_task(self, task_id: int) -> APIResponse:
        """PUT /VMware/vmware/restore_task/{task_id}/stop"""
        return self.client.put(f"/VMware/vmware/restore_task/{task_id}/stop")

    def delete_restore_task(self, task_id: int) -> APIResponse:
        """DELETE /VMware/vmware/restore_task/{task_id}"""
        return self.client.delete(f"/VMware/vmware/restore_task/{task_id}")

    # ── 概览 (1) ──────────────────────────────────────
    def overview(self) -> APIResponse:
        """GET /VMware/vmware/overview"""
        return self.client.get("/VMware/vmware/overview")
