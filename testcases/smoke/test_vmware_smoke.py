"""
L1 冒烟测试 - VMware 模块
覆盖所有 41 个 API 用例 (CB-054 ~ CB-094)

每个用例至少一个测试方法，使用 pytest + vmware_api fixture。
"""

import pytest

pytestmark = pytest.mark.smoke


# ═══════════════════════════════════════════════════════
# 概览
# ═══════════════════════════════════════════════════════
class TestVMwareOverview:
    """概览 - CB-094"""

    def test_overview_ok(self, vmware_api):
        """CB-094: GET /VMware/vmware/overview"""
        resp = vmware_api.overview()
        assert resp.ok, f"overview failed: {resp.message}"
        assert isinstance(resp.data, dict)


# ═══════════════════════════════════════════════════════
# 设备管理 — 查询
# ═══════════════════════════════════════════════════════
class TestVMwareDeviceList:
    """设备查询 - CB-054, CB-055"""

    def test_list_devices(self, vmware_api):
        """CB-054: GET /VMware/vmware/device"""
        resp = vmware_api.list_devices()
        assert resp.ok, f"list_devices failed: {resp.message}"

    def test_list_devices_update_status(self, vmware_api):
        """CB-054 (变体): GET /VMware/vmware/device?update_status=true"""
        resp = vmware_api.list_devices(update_status=True)
        assert resp.status_code == 200

    def test_get_device(self, vmware_api):
        """CB-055: GET /VMware/vmware/device/{device_id}"""
        resp = vmware_api.get_device(1)
        assert resp.ok or resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 设备管理 — 添加/删除
# ═══════════════════════════════════════════════════════
class TestVMwareDeviceAdd:
    """添加设备 - CB-056"""

    def test_add_device(self, vmware_api):
        """CB-056: POST /VMware/vmware/device"""
        resp = vmware_api.add_device({
            "name": "VMware-Server-1",
            "port": 443,
            "ip": "10.18.8.10",
            "user": "admin",
            "password": "password",
        })
        assert resp.status_code == 200


class TestVMwareDeviceDelete:
    """删除设备 - CB-057"""

    def test_delete_device(self, vmware_api):
        """CB-057: DELETE /VMware/vmware/device/{device_id}"""
        resp = vmware_api.delete_device(999999)
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 设备管理 — 检查
# ═══════════════════════════════════════════════════════
class TestVMwareDeviceCheck:
    """设备检查 - CB-058, CB-059, CB-060"""

    def test_check_resource_enough(self, vmware_api):
        """CB-058: POST /VMware/vmware/device/check_resource_is_enough"""
        resp = vmware_api.check_resource_enough({})
        assert resp.status_code == 200

    def test_check_restore_support(self, vmware_api):
        """CB-059: POST /VMware/vmware/device/check_restore_is_support"""
        resp = vmware_api.check_restore_support({})
        assert resp.status_code == 200

    def test_check_vm_exist(self, vmware_api):
        """CB-060: POST /VMware/vmware/device/check_vm_is_exist"""
        resp = vmware_api.check_vm_exist({})
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 设备管理 — 状态/关联
# ═══════════════════════════════════════════════════════
class TestVMwareDeviceStatus:
    """设备状态 - CB-061, CB-062"""

    def test_get_device_status(self, vmware_api):
        """CB-061: GET /VMware/vmware/device/{device_id}/device_status"""
        resp = vmware_api.get_device_status(1)
        assert resp.status_code == 200

    def test_get_linked_task(self, vmware_api):
        """CB-062: GET /VMware/vmware/device/{device_id}/be_linked_task"""
        resp = vmware_api.get_linked_task(1)
        assert resp.status_code == 200


class TestVMwareTaskDevices:
    """任务设备 - CB-063"""

    def test_get_task_devices(self, vmware_api):
        """CB-063: GET /VMware/vmware/get_task_devices/"""
        resp = vmware_api.get_task_devices()
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 数据中心浏览
# ═══════════════════════════════════════════════════════
class TestVMwareDatacenters:
    """数据中心 - CB-064"""

    def test_list_datacenters(self, vmware_api):
        """CB-064: GET /VMware/vmware/device/datacenters/{device_id}"""
        resp = vmware_api.list_datacenters(1)
        assert resp.status_code == 200


class TestVMwareDatacenterClusters:
    """集群 - CB-065, CB-066, CB-067"""

    def test_list_datacenter_clusters(self, vmware_api):
        """CB-065: POST /VMware/vmware/device/datacenter_clusters"""
        resp = vmware_api.list_datacenter_clusters({"device_id": 1, "datacenter_id": "dc-1"})
        assert resp.status_code == 200

    def test_list_datacenter_cluster_hosts(self, vmware_api):
        """CB-066: POST /VMware/vmware/device/datacenter_cluster_hosts"""
        resp = vmware_api.list_datacenter_cluster_hosts({"device_id": 1, "datacenter_id": "dc-1", "cluster_id": "cl-1"})
        assert resp.status_code == 200

    def test_list_datacenter_cluster_host_vms(self, vmware_api):
        """CB-067: POST /VMware/vmware/device/datacenter_cluster_host_vms"""
        resp = vmware_api.list_datacenter_cluster_host_vms(
            {"device_id": 1, "datacenter_id": "dc-1", "cluster_id": "cl-1", "host_id": "host-1"}
        )
        assert resp.status_code == 200


class TestVMwareDatacenterFolders:
    """文件夹 - CB-068, CB-069"""

    def test_list_datacenter_folders(self, vmware_api):
        """CB-068: POST /VMware/vmware/device/datacenter_folders"""
        resp = vmware_api.list_datacenter_folders({"device_id": 1, "datacenter_id": "dc-1"})
        assert resp.status_code == 200

    def test_list_datacenter_folder_vms(self, vmware_api):
        """CB-069: POST /VMware/vmware/device/datacenter_folder_vms"""
        resp = vmware_api.list_datacenter_folder_vms(
            {"device_id": 1, "datacenter_id": "dc-1", "folder_id": "folder-1"}
        )
        assert resp.status_code == 200


class TestVMwareDatacenterInfra:
    """数据存储/网络/VM - CB-070, CB-071, CB-072, CB-073"""

    def test_list_datacenter_datastores(self, vmware_api):
        """CB-070: POST /VMware/vmware/device/datacenter_datastores"""
        resp = vmware_api.list_datacenter_datastores({"device_id": 1, "datacenter_id": "dc-1"})
        assert resp.status_code == 200

    def test_list_datacenter_networks(self, vmware_api):
        """CB-071: POST /VMware/vmware/device/datacenter_networks"""
        resp = vmware_api.list_datacenter_networks({"device_id": 1, "datacenter_id": "dc-1"})
        assert resp.status_code == 200

    def test_list_datacenter_vms(self, vmware_api):
        """CB-072: POST /VMware/vmware/device/datacenter_vms"""
        resp = vmware_api.list_datacenter_vms({"device_id": 1, "datacenter_id": "dc-1"})
        assert resp.status_code == 200

    def test_get_datacenter_vm(self, vmware_api):
        """CB-073: POST /VMware/vmware/device/datacenter_vm"""
        resp = vmware_api.get_datacenter_vm({"device_id": 1, "datacenter_id": "dc-1", "vm_id": "vm-1"})
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# VM列表查询
# ═══════════════════════════════════════════════════════
class TestVMwareVMList:
    """VM查询 - CB-074"""

    def test_list_vms(self, vmware_api):
        """CB-074: GET /VMware/vmware/vm_list"""
        resp = vmware_api.list_vms()
        assert resp.status_code == 200

    def test_list_vms_by_device(self, vmware_api):
        """CB-074 (变体): GET /VMware/vmware/vm_list?id={device_id}"""
        resp = vmware_api.list_vms(device_id=1)
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 任务管理 — 查询/创建/导入
# ═══════════════════════════════════════════════════════
class TestVMwareTaskList:
    """任务查询 - CB-075, CB-076"""

    def test_list_tasks(self, vmware_api):
        """CB-075: GET /VMware/vmware/task"""
        resp = vmware_api.list_tasks()
        assert resp.ok, f"list_tasks failed: {resp.message}"

    def test_get_task(self, vmware_api):
        """CB-076: GET /VMware/vmware/task/{task_id}"""
        resp = vmware_api.get_task(1)
        assert resp.status_code == 200


class TestVMwareTaskAdd:
    """添加任务 - CB-077"""

    def test_add_task(self, vmware_api):
        """CB-077: POST /VMware/vmware/task"""
        resp = vmware_api.add_task({
            "name": "VMware-Task-1",
            "device_id": 1,
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "version_strategy": {"is_enabled": False, "max_num": 2},
        })
        assert resp.status_code == 200


class TestVMwareTaskImport:
    """导入任务 - CB-078"""

    def test_import_task(self, vmware_api):
        """CB-078: POST /VMware/vmware/task/import"""
        resp = vmware_api.import_task({
            "path": "/Volume1/public/VMwareBackup",
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 任务管理 — 启动/停止
# ═══════════════════════════════════════════════════════
class TestVMwareTaskStartStop:
    """启动/停止任务 - CB-079, CB-080"""

    def test_start_task(self, vmware_api):
        """CB-079: PUT /VMware/vmware/task/{task_id}/start"""
        resp = vmware_api.start_task(1)
        assert resp.status_code == 200

    def test_stop_task(self, vmware_api):
        """CB-080: PUT /VMware/vmware/task/{task_id}/stop"""
        resp = vmware_api.stop_task(1)
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 任务管理 — 检查
# ═══════════════════════════════════════════════════════
class TestVMwareTaskCheck:
    """任务检查 - CB-081, CB-082"""

    def test_check_dest_folder(self, vmware_api):
        """CB-081: POST /VMware/vmware/task/check_dest_folder"""
        resp = vmware_api.check_dest_folder({})
        assert resp.status_code == 200

    def test_check_vm_service(self, vmware_api):
        """CB-082: POST /VMware/vmware/task/check_vm_service"""
        resp = vmware_api.check_vm_service({})
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 任务管理 — 磁盘/分区/版本VM
# ═══════════════════════════════════════════════════════
class TestVMwareTaskDiskPartition:
    """磁盘分区 - CB-083, CB-084, CB-085"""

    def test_get_disk_partitions(self, vmware_api):
        """CB-083: POST /VMware/vmware/task/get_disk_partitions"""
        resp = vmware_api.get_disk_partitions({})
        assert resp.status_code == 200

    def test_get_partition_system(self, vmware_api):
        """CB-084: POST /VMware/vmware/task/get_partition_system"""
        resp = vmware_api.get_partition_system({})
        assert resp.status_code == 200

    def test_get_task_ver_vms(self, vmware_api):
        """CB-085: POST /VMware/vmware/task/get_task_ver_vms"""
        resp = vmware_api.get_task_ver_vms({})
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 版本管理
# ═══════════════════════════════════════════════════════
class TestVMwareVersionList:
    """版本查询 - CB-086, CB-087"""

    def test_list_versions(self, vmware_api):
        """CB-086: GET /VMware/vmware/task/version/{task_id}"""
        resp = vmware_api.list_versions(1)
        assert resp.status_code == 200

    def test_list_all_versions(self, vmware_api):
        """CB-087: GET /VMware/vmware/task/version"""
        resp = vmware_api.list_all_versions()
        assert resp.status_code == 200

    def test_list_all_versions_by_id(self, vmware_api):
        """CB-087 (变体): GET /VMware/vmware/task/version?id={}"""
        resp = vmware_api.list_all_versions(task_id=1)
        assert resp.status_code == 200


class TestVMwareVersionLock:
    """版本锁定 - CB-088"""

    def test_set_ver_locked(self, vmware_api):
        """CB-088: POST /VMware/vmware/task/version/set_ver_locked"""
        resp = vmware_api.set_ver_locked(1, True)
        assert resp.status_code == 200

    def test_set_ver_unlocked(self, vmware_api):
        """CB-088 (解锁): POST /VMware/vmware/task/version/set_ver_locked"""
        resp = vmware_api.set_ver_locked(1, False)
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 还原任务
# ═══════════════════════════════════════════════════════
class TestVMwareRestoreList:
    """还原任务查询 - CB-089, CB-090"""

    def test_list_restore_tasks(self, vmware_api):
        """CB-089: GET /VMware/vmware/restore_task"""
        resp = vmware_api.list_restore_tasks()
        assert resp.ok, f"list_restore_tasks failed: {resp.message}"

    def test_get_restore_task(self, vmware_api):
        """CB-090: GET /VMware/vmware/restore_task/{task_id}"""
        resp = vmware_api.get_restore_task(1)
        assert resp.status_code == 200


class TestVMwareRestoreStartStop:
    """还原启动/停止 - CB-091, CB-092"""

    def test_start_restore_task(self, vmware_api):
        """CB-091: PUT /VMware/vmware/restore_task/{task_id}/start"""
        resp = vmware_api.start_restore_task(1)
        assert resp.status_code == 200

    def test_stop_restore_task(self, vmware_api):
        """CB-092: PUT /VMware/vmware/restore_task/{task_id}/stop"""
        resp = vmware_api.stop_restore_task(1)
        assert resp.status_code == 200


class TestVMwareRestoreDelete:
    """还原删除 - CB-093"""

    def test_delete_restore_task(self, vmware_api):
        """CB-093: DELETE /VMware/vmware/restore_task/{task_id}"""
        resp = vmware_api.delete_restore_task(1)
        assert resp.status_code == 200
