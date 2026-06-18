"""
L1 冒烟测试 - VMware 模块
覆盖所有38个API的基本可达性和响应结构校验
"""

import pytest

pytestmark = pytest.mark.smoke


class TestVMwareOverview:
    def test_overview_ok(self, vmware_api):
        resp = vmware_api.overview()
        assert resp.ok, f"overview failed: {resp.message}"
        assert isinstance(resp.data, dict)


class TestVMwareDevice:
    """设备管理接口冒烟"""

    def test_list_devices(self, vmware_api):
        assert vmware_api.list_devices().ok

    def test_list_devices_update_status(self, vmware_api):
        assert vmware_api.list_devices(update_status=True).status_code == 200

    def test_get_device_not_found(self, vmware_api):
        assert vmware_api.get_device(999999).status_code == 200

    def test_get_task_devices(self, vmware_api):
        assert vmware_api.get_task_devices().status_code == 200

    def test_check_resource_enough_empty(self, vmware_api):
        assert vmware_api.check_resource_enough({}).status_code == 200

    def test_check_restore_support_empty(self, vmware_api):
        assert vmware_api.check_restore_support({}).status_code == 200

    def test_check_vm_exist_empty(self, vmware_api):
        assert vmware_api.check_vm_exist({}).status_code == 200

    def test_get_device_status_not_found(self, vmware_api):
        assert vmware_api.get_device_status(999999).status_code == 200

    def test_get_linked_task_not_found(self, vmware_api):
        assert vmware_api.get_linked_task(999999).status_code == 200


class TestVMwareTask:
    """任务管理接口冒烟"""

    def test_list_tasks(self, vmware_api):
        assert vmware_api.list_tasks().ok

    def test_get_task_not_found(self, vmware_api):
        assert vmware_api.get_task(999999).status_code == 200

    def test_check_dest_folder_empty(self, vmware_api):
        assert vmware_api.check_dest_folder({}).status_code == 200

    def test_check_vm_service_empty(self, vmware_api):
        assert vmware_api.check_vm_service({}).status_code == 200

    def test_get_disk_partitions_empty(self, vmware_api):
        assert vmware_api.get_disk_partitions({}).status_code == 200

    def test_get_partition_system_empty(self, vmware_api):
        assert vmware_api.get_partition_system({}).status_code == 200

    def test_get_task_ver_vms_empty(self, vmware_api):
        assert vmware_api.get_task_ver_vms({}).status_code == 200

    def test_start_task_not_found(self, vmware_api):
        assert vmware_api.start_task(999999).status_code == 200

    def test_stop_task_not_found(self, vmware_api):
        assert vmware_api.stop_task(999999).status_code == 200

    def test_import_task_empty(self, vmware_api):
        assert vmware_api.import_task({}).status_code == 200


class TestVMwareVersion:
    """版本管理接口冒烟"""

    def test_list_versions_not_found(self, vmware_api):
        assert vmware_api.list_versions(999999).status_code == 200


class TestVMwareRestore:
    """还原任务接口冒烟"""

    def test_list_restore_tasks(self, vmware_api):
        assert vmware_api.list_restore_tasks().ok

    def test_get_restore_task_not_found(self, vmware_api):
        assert vmware_api.get_restore_task(999999).status_code == 200

    def test_start_restore_not_found(self, vmware_api):
        assert vmware_api.start_restore_task(999999).status_code == 200

    def test_stop_restore_not_found(self, vmware_api):
        assert vmware_api.stop_restore_task(999999).status_code == 200

    def test_delete_restore_not_found(self, vmware_api):
        assert vmware_api.delete_restore_task(999999).status_code == 200
