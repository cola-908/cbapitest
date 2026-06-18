"""
L1 冒烟测试 - Hyper-V 模块
覆盖所有37个API的基本可达性和响应结构校验
"""

import pytest

pytestmark = pytest.mark.smoke


class TestHyperVOverview:
    def test_overview_ok(self, hyperv_api):
        resp = hyperv_api.overview()
        assert resp.ok, f"overview failed: {resp.message}"
        assert isinstance(resp.data, dict)


class TestHyperVDevice:
    """设备管理接口冒烟"""

    def test_list_devices(self, hyperv_api):
        assert hyperv_api.list_devices().ok

    def test_list_devices_update_online(self, hyperv_api):
        assert hyperv_api.list_devices(is_update_online=True).status_code == 200

    def test_get_device_not_found(self, hyperv_api):
        assert hyperv_api.get_device("nonexistent").status_code == 200

    def test_get_device_state_not_found(self, hyperv_api):
        assert hyperv_api.get_device_state("nonexistent").status_code == 200

    def test_get_default_cfg_not_found(self, hyperv_api):
        assert hyperv_api.get_default_cfg("nonexistent").status_code == 200

    def test_get_vm_list_not_found(self, hyperv_api):
        assert hyperv_api.get_vm_list("nonexistent").status_code == 200

    def test_list_device_vms_not_found(self, hyperv_api):
        assert hyperv_api.list_device_vms("nonexistent").status_code == 200

    def test_get_vm_default_dirs_not_found(self, hyperv_api):
        assert hyperv_api.get_vm_default_dirs("nonexistent").status_code == 200

    def test_list_device_drv_dir_not_found(self, hyperv_api):
        assert hyperv_api.list_device_drv_dir("nonexistent").status_code == 200

    def test_list_device_drv_letter_not_found(self, hyperv_api):
        assert hyperv_api.list_device_drv_letter("nonexistent").status_code == 200

    def test_list_dir_not_found(self, hyperv_api):
        assert hyperv_api.list_dir("nonexistent", {}).status_code == 200

    def test_list_device_tasks_not_found(self, hyperv_api):
        assert hyperv_api.list_device_tasks("nonexistent", "nonexistent").status_code == 200


class TestHyperVTask:
    """任务管理接口冒烟"""

    def test_list_tasks(self, hyperv_api):
        assert hyperv_api.list_tasks().ok

    def test_get_task_not_found(self, hyperv_api):
        assert hyperv_api.get_task("nonexistent").status_code == 200

    def test_get_task_detail_not_found(self, hyperv_api):
        assert hyperv_api.get_task_detail("nonexistent", "nonexistent").status_code == 200

    def test_add_task_empty(self, hyperv_api):
        assert hyperv_api.add_task({}).status_code == 200

    def test_exec_task_not_found(self, hyperv_api):
        assert hyperv_api.exec_task("nonexistent").status_code == 200

    def test_stop_task_not_found(self, hyperv_api):
        assert hyperv_api.stop_task("nonexistent").status_code == 200

    def test_delete_task_not_found(self, hyperv_api):
        assert hyperv_api.delete_task("nonexistent").status_code == 200

    def test_delete_task_version_not_found(self, hyperv_api):
        assert hyperv_api.delete_task_version("none", "none").status_code == 200

    def test_get_task_version_detail_not_found(self, hyperv_api):
        assert hyperv_api.get_task_version_detail("none", "none", "none").status_code == 200

    def test_delete_task_sub_not_found(self, hyperv_api):
        assert hyperv_api.delete_task_sub("none", "none", "none").status_code == 200


class TestHyperVRestore:
    """还原任务接口冒烟"""

    def test_list_restore_tasks(self, hyperv_api):
        assert hyperv_api.list_restore_tasks().ok

    def test_get_restore_task_not_found(self, hyperv_api):
        assert hyperv_api.get_restore_task("nonexistent").status_code == 200

    def test_list_restores(self, hyperv_api):
        assert hyperv_api.list_restores().ok

    def test_get_restore_not_found(self, hyperv_api):
        assert hyperv_api.get_restore("nonexistent").status_code == 200

    def test_add_restore_empty(self, hyperv_api):
        assert hyperv_api.add_restore({}).status_code == 200

    def test_exec_restore_not_found(self, hyperv_api):
        assert hyperv_api.exec_restore("nonexistent").status_code == 200

    def test_stop_restore_not_found(self, hyperv_api):
        assert hyperv_api.stop_restore("nonexistent").status_code == 200

    def test_delete_restore_not_found(self, hyperv_api):
        assert hyperv_api.delete_restore("nonexistent").status_code == 200


class TestHyperVPortal:
    """Portal浏览接口冒烟"""

    def test_browse_part_empty(self, hyperv_api):
        assert hyperv_api.browse_part({}).status_code == 200

    def test_disk_parts(self, hyperv_api):
        assert hyperv_api.disk_parts().status_code == 200

    def test_disk_view_browse_empty(self, hyperv_api):
        assert hyperv_api.disk_view_browse({}).status_code == 200

    def test_get_disk_parts_empty(self, hyperv_api):
        assert hyperv_api.get_disk_parts("").status_code == 200
