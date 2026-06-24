"""
VMware API - 覆盖41个测试用例

代理路径前缀 /VMware → /v2/proxy2/CentralizedBackup

用例覆盖:
  CB-054: GET  /vmware/device                        查询设备列表
  CB-055: GET  /vmware/device/{device_id}            查询单个设备
  CB-056: POST /vmware/device                        添加设备
  CB-057: DELETE /vmware/device/{device_id}          删除设备
  CB-058: POST /vmware/device/check_resource_is_enough  检查资源
  CB-059: POST /vmware/device/check_restore_is_support  检查还原支持
  CB-060: POST /vmware/device/check_vm_is_exist      检查VM存在
  CB-061: GET  /vmware/device/{device_id}/device_status  设备状态
  CB-062: GET  /vmware/device/{device_id}/be_linked_task 关联任务
  CB-063: GET  /vmware/get_task_devices/             任务设备
  CB-064: GET  /vmware/device/datacenters/{device_id}  数据中心
  CB-065: POST /vmware/device/datacenter_clusters    集群
  CB-066: POST /vmware/device/datacenter_cluster_hosts  主机
  CB-067: POST /vmware/device/datacenter_cluster_host_vms  主机VM
  CB-068: POST /vmware/device/datacenter_folders     文件夹
  CB-069: POST /vmware/device/datacenter_folder_vms  文件夹VM
  CB-070: POST /vmware/device/datacenter_datastores  数据存储
  CB-071: POST /vmware/device/datacenter_networks    网络
  CB-072: POST /vmware/device/datacenter_vms         VM列表
  CB-073: POST /vmware/device/datacenter_vm          单个VM
  CB-074: GET  /vmware/vm_list                       VM查询
  CB-075: GET  /vmware/task                          任务列表
  CB-076: GET  /vmware/task/{task_id}                单个任务
  CB-077: POST /vmware/task                          添加任务
  CB-078: POST /vmware/task/import                   导入任务
  CB-079: PUT  /vmware/task/{task_id}/start          启动任务
  CB-080: PUT  /vmware/task/{task_id}/stop           停止任务
  CB-081: POST /vmware/task/check_dest_folder        检查目标文件夹
  CB-082: POST /vmware/task/check_vm_service         检查VM服务
  CB-083: POST /vmware/task/get_disk_partitions      磁盘分区
  CB-084: POST /vmware/task/get_partition_system     分区系统
  CB-085: POST /vmware/task/get_task_ver_vms         版本VM
  CB-086: GET  /vmware/task/version/{task_id}        任务版本
  CB-087: GET  /vmware/task/version                  全部版本
  CB-088: POST /vmware/task/version/set_ver_locked   版本锁定
  CB-089: GET  /vmware/restore_task                  还原任务列表
  CB-090: GET  /vmware/restore_task/{task_id}        单个还原任务
  CB-091: PUT  /vmware/restore_task/{task_id}/start  启动还原
  CB-092: PUT  /vmware/restore_task/{task_id}/stop   停止还原
  CB-093: DELETE /vmware/restore_task/{task_id}      删除还原
  CB-094: GET  /vmware/overview                      概览
"""

from typing import Any, Optional
from client.base import TOSHttpClient, APIResponse


class VMwareAPI:
    """VMware 虚拟机备份还原 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ══════════════════════════════════════════════════════
    # 设备管理
    # ══════════════════════════════════════════════════════
    def list_devices(self, update_status: Optional[bool] = None) -> APIResponse:
        """GET /VMware/vmware/device
        覆盖: CB-054
        """
        params = {"update_status": "true" if update_status else "false"} if update_status is not None else None
        return self.client.get("/VMware/vmware/device", params=params)

    def get_device(self, device_id: str | int) -> APIResponse:
        """GET /VMware/vmware/device/{device_id}
        覆盖: CB-055
        """
        return self.client.get(f"/VMware/vmware/device/{device_id}")

    def add_device(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device
        覆盖: CB-056
        """
        return self.client.post("/VMware/vmware/device", json=data)

    def delete_device(self, device_id: str | int) -> APIResponse:
        """DELETE /VMware/vmware/device/{device_id}
        覆盖: CB-057
        """
        return self.client.delete(f"/VMware/vmware/device/{device_id}")

    def check_resource_enough(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/check_resource_is_enough
        覆盖: CB-058
        """
        return self.client.post("/VMware/vmware/device/check_resource_is_enough", json=data)

    def check_restore_support(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/check_restore_is_support
        覆盖: CB-059
        """
        return self.client.post("/VMware/vmware/device/check_restore_is_support", json=data)

    def check_vm_exist(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/check_vm_is_exist
        覆盖: CB-060
        """
        return self.client.post("/VMware/vmware/device/check_vm_is_exist", json=data)

    def get_device_status(self, device_id: str | int) -> APIResponse:
        """GET /VMware/vmware/device/{device_id}/device_status
        覆盖: CB-061
        """
        return self.client.get(f"/VMware/vmware/device/{device_id}/device_status")

    def get_linked_task(self, device_id: str | int) -> APIResponse:
        """GET /VMware/vmware/device/{device_id}/be_linked_task
        覆盖: CB-062
        """
        return self.client.get(f"/VMware/vmware/device/{device_id}/be_linked_task")

    def get_task_devices(self) -> APIResponse:
        """GET /VMware/vmware/get_task_devices/
        覆盖: CB-063
        """
        return self.client.get("/VMware/vmware/get_task_devices/")

    # ── 数据中心浏览 ────────────────────────────────────
    def list_datacenters(self, device_id: str | int) -> APIResponse:
        """GET /VMware/vmware/device/datacenters/{device_id}
        覆盖: CB-064
        """
        return self.client.get(f"/VMware/vmware/device/datacenters/{device_id}")

    def list_datacenter_clusters(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_clusters
        覆盖: CB-065
        """
        return self.client.post("/VMware/vmware/device/datacenter_clusters", json=data)

    def list_datacenter_cluster_hosts(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_cluster_hosts
        覆盖: CB-066
        """
        return self.client.post("/VMware/vmware/device/datacenter_cluster_hosts", json=data)

    def list_datacenter_cluster_host_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_cluster_host_vms
        覆盖: CB-067
        """
        return self.client.post("/VMware/vmware/device/datacenter_cluster_host_vms", json=data)

    def list_datacenter_folders(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_folders
        覆盖: CB-068
        """
        return self.client.post("/VMware/vmware/device/datacenter_folders", json=data)

    def list_datacenter_folder_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_folder_vms
        覆盖: CB-069
        """
        return self.client.post("/VMware/vmware/device/datacenter_folder_vms", json=data)

    def list_datacenter_datastores(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_datastores
        覆盖: CB-070
        """
        return self.client.post("/VMware/vmware/device/datacenter_datastores", json=data)

    def list_datacenter_networks(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_networks
        覆盖: CB-071
        """
        return self.client.post("/VMware/vmware/device/datacenter_networks", json=data)

    def list_datacenter_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_vms
        覆盖: CB-072
        """
        return self.client.post("/VMware/vmware/device/datacenter_vms", json=data)

    def get_datacenter_vm(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/device/datacenter_vm
        覆盖: CB-073
        """
        return self.client.post("/VMware/vmware/device/datacenter_vm", json=data)

    def list_vms(self, device_id: Optional[str | int] = None) -> APIResponse:
        """GET /VMware/vmware/vm_list?id={device_id}
        覆盖: CB-074
        """
        params = {"id": device_id} if device_id else None
        return self.client.get("/VMware/vmware/vm_list", params=params)

    # ══════════════════════════════════════════════════════
    # 任务管理
    # ══════════════════════════════════════════════════════
    def list_tasks(self) -> APIResponse:
        """GET /VMware/vmware/task
        覆盖: CB-075
        """
        return self.client.get("/VMware/vmware/task")

    def get_task(self, task_id: str | int) -> APIResponse:
        """GET /VMware/vmware/task/{task_id}
        覆盖: CB-076
        """
        return self.client.get(f"/VMware/vmware/task/{task_id}")

    def add_task(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task
        覆盖: CB-077
        """
        return self.client.post("/VMware/vmware/task", json=data)

    def import_task(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/import
        覆盖: CB-078
        """
        return self.client.post("/VMware/vmware/task/import", json=data)

    def start_task(self, task_id: str | int) -> APIResponse:
        """PUT /VMware/vmware/task/{task_id}/start
        覆盖: CB-079
        """
        return self.client.put(f"/VMware/vmware/task/{task_id}/start")

    def stop_task(self, task_id: str | int) -> APIResponse:
        """PUT /VMware/vmware/task/{task_id}/stop
        覆盖: CB-080
        """
        return self.client.put(f"/VMware/vmware/task/{task_id}/stop")

    def check_dest_folder(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/check_dest_folder
        覆盖: CB-081
        """
        return self.client.post("/VMware/vmware/task/check_dest_folder", json=data)

    def check_vm_service(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/check_vm_service
        覆盖: CB-082
        """
        return self.client.post("/VMware/vmware/task/check_vm_service", json=data)

    def get_disk_partitions(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/get_disk_partitions
        覆盖: CB-083
        """
        return self.client.post("/VMware/vmware/task/get_disk_partitions", json=data)

    def get_partition_system(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/get_partition_system
        覆盖: CB-084
        """
        return self.client.post("/VMware/vmware/task/get_partition_system", json=data)

    def get_task_ver_vms(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/get_task_ver_vms
        覆盖: CB-085
        """
        return self.client.post("/VMware/vmware/task/get_task_ver_vms", json=data)

    # ══════════════════════════════════════════════════════
    # 版本管理
    # ══════════════════════════════════════════════════════
    def list_versions(self, task_id: str | int) -> APIResponse:
        """GET /VMware/vmware/task/version/{task_id}
        覆盖: CB-086
        """
        return self.client.get(f"/VMware/vmware/task/version/{task_id}")

    def list_all_versions(self, task_id: Optional[str | int] = None) -> APIResponse:
        """GET /VMware/vmware/task/version?id={task_id}
        覆盖: CB-087
        """
        params = {"id": task_id} if task_id else None
        return self.client.get("/VMware/vmware/task/version", params=params)

    def set_ver_locked(self, ver_id: str | int, locked: bool) -> APIResponse:
        """POST /VMware/vmware/task/version/set_ver_locked
        覆盖: CB-088
        """
        return self.client.post(
            "/VMware/vmware/task/version/set_ver_locked",
            json={"id": ver_id, "locked": locked},
        )

    def set_ver_locked_raw(self, data: dict) -> APIResponse:
        """POST /VMware/vmware/task/version/set_ver_locked
        覆盖: CB-088 (raw body)
        """
        return self.client.post("/VMware/vmware/task/version/set_ver_locked", json=data)

    # ══════════════════════════════════════════════════════
    # 还原任务
    # ══════════════════════════════════════════════════════
    def list_restore_tasks(self) -> APIResponse:
        """GET /VMware/vmware/restore_task
        覆盖: CB-089
        """
        return self.client.get("/VMware/vmware/restore_task")

    def get_restore_task(self, task_id: str | int) -> APIResponse:
        """GET /VMware/vmware/restore_task/{task_id}
        覆盖: CB-090
        """
        return self.client.get(f"/VMware/vmware/restore_task/{task_id}")

    def start_restore_task(self, task_id: str | int) -> APIResponse:
        """PUT /VMware/vmware/restore_task/{task_id}/start
        覆盖: CB-091
        """
        return self.client.put(f"/VMware/vmware/restore_task/{task_id}/start")

    def stop_restore_task(self, task_id: str | int) -> APIResponse:
        """PUT /VMware/vmware/restore_task/{task_id}/stop
        覆盖: CB-092
        """
        return self.client.put(f"/VMware/vmware/restore_task/{task_id}/stop")

    def delete_restore_task(self, task_id: str | int) -> APIResponse:
        """DELETE /VMware/vmware/restore_task/{task_id}
        覆盖: CB-093
        """
        return self.client.delete(f"/VMware/vmware/restore_task/{task_id}")

    # ══════════════════════════════════════════════════════
    # 概览
    # ══════════════════════════════════════════════════════
    def overview(self) -> APIResponse:
        """GET /VMware/vmware/overview
        覆盖: CB-094
        """
        return self.client.get("/VMware/vmware/overview")
