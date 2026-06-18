"""
L1 冒烟测试 - PC/Server (Win) 模块
覆盖所有39个API的基本可达性和响应结构校验
"""

import pytest

pytestmark = pytest.mark.smoke


class TestWinOverview:
    """概览接口冒烟"""

    def test_overview_ok(self, win_api):
        resp = win_api.overview()
        assert resp.ok, f"overview failed: {resp.message}"
        assert isinstance(resp.data, dict)
        assert "device" in resp.data
        assert "tasks" in resp.data


class TestWinDevice:
    """设备管理接口冒烟（8个）"""

    def test_list_devices(self, win_api):
        resp = win_api.list_devices()
        assert resp.ok, f"list_devices failed: {resp.message}"

    def test_list_devices_by_type(self, win_api):
        resp = win_api.list_devices(device_type="desktop")
        assert resp.ok

    def test_list_all_devices(self, win_api):
        resp = win_api.list_all_devices()
        assert resp.ok

    def test_get_device_not_found(self, win_api):
        resp = win_api.get_device("nonexistent-id")
        # 不存在的设备，接口不应500
        assert resp.status_code == 200

    def test_get_device_volumes_not_found(self, win_api):
        resp = win_api.get_device_volumes("nonexistent-id")
        assert resp.status_code == 200

    def test_upgrade_device_not_found(self, win_api):
        resp = win_api.upgrade_device("nonexistent-id")
        assert resp.status_code == 200

    def test_get_device_tasks_summary_not_found(self, win_api):
        resp = win_api.get_device_tasks_summary("nonexistent-id")
        assert resp.status_code == 200

    def test_batch_delete_devices_empty(self, win_api):
        resp = win_api.batch_delete_devices([])
        assert resp.status_code == 200


class TestWinTask:
    """任务管理接口冒烟（13个）"""

    def test_list_tasks(self, win_api):
        resp = win_api.list_tasks()
        assert resp.ok

    def test_list_tasks_by_type(self, win_api):
        resp = win_api.list_tasks(task_type="desktop")
        assert resp.ok

    def test_list_all_tasks(self, win_api):
        resp = win_api.list_all_tasks()
        assert resp.ok

    def test_get_task_not_found(self, win_api):
        resp = win_api.get_task(999999)
        assert resp.status_code == 200

    def test_exec_task_not_found(self, win_api):
        resp = win_api.exec_task(999999)
        assert resp.status_code == 200

    def test_cancel_task_not_found(self, win_api):
        resp = win_api.cancel_task(999999)
        assert resp.status_code == 200

    def test_get_task_verbose_not_found(self, win_api):
        resp = win_api.get_task_verbose(999999)
        assert resp.status_code == 200

    def test_relink_task(self, win_api):
        resp = win_api.relink_task("desktop")
        assert resp.status_code == 200

    def test_batch_exec_tasks_empty(self, win_api):
        resp = win_api.batch_exec_tasks([])
        assert resp.status_code == 200

    def test_batch_cancel_tasks_empty(self, win_api):
        resp = win_api.batch_cancel_tasks([])
        assert resp.status_code == 200

    def test_batch_delete_tasks_empty(self, win_api):
        resp = win_api.batch_delete_tasks([])
        assert resp.status_code == 200

    def test_batch_add_tasks_empty(self, win_api):
        resp = win_api.batch_add_tasks([])
        assert resp.status_code == 200

    def test_batch_edit_tasks_empty(self, win_api):
        resp = win_api.batch_edit_tasks([])
        assert resp.status_code == 200


class TestWinVersion:
    """版本管理接口冒烟（6个）"""

    def test_list_versions_not_found(self, win_api):
        resp = win_api.list_versions("nonexistent", 999999)
        assert resp.status_code == 200

    def test_get_version_not_found(self, win_api):
        resp = win_api.get_version("nonexistent", 999999, "nonexistent")
        assert resp.status_code == 200

    def test_get_version_guide_not_found(self, win_api):
        resp = win_api.get_version_guide("nonexistent", 999999)
        assert resp.status_code == 200

    def test_get_version_detail_not_found(self, win_api):
        resp = win_api.get_version_detail("nonexistent", 999999, "nonexistent")
        assert resp.status_code == 200

    def test_get_disk_partitions_not_found(self, win_api):
        resp = win_api.get_disk_partitions("none", 0, "none", "none", "none")
        assert resp.status_code == 200

    def test_get_device_task_versions_not_found(self, win_api):
        resp = win_api.get_device_task_versions("nonexistent", 999999)
        assert resp.status_code == 200


class TestWinRestore:
    """还原接口冒烟（5个）"""

    def test_list_restore_tasks(self, win_api):
        resp = win_api.list_restore_tasks()
        assert resp.ok

    def test_cancel_restore_not_found(self, win_api):
        resp = win_api.cancel_restore(999999)
        assert resp.status_code == 200

    def test_delete_restore_not_found(self, win_api):
        resp = win_api.delete_restore(999999)
        assert resp.status_code == 200

    def test_create_restore_empty(self, win_api):
        resp = win_api.create_restore_task({})
        assert resp.status_code == 200

    def test_restore_empty(self, win_api):
        resp = win_api.restore({})
        assert resp.status_code == 200


class TestWinPortal:
    """Portal浏览接口冒烟（5个）"""

    def test_browse_image_not_found(self, win_api):
        resp = win_api.browse_image("nonexistent")
        assert resp.status_code == 200

    def test_get_dev_dir_sub_dirs_not_found(self, win_api):
        resp = win_api.get_dev_dir_sub_dirs("nonexistent")
        assert resp.status_code == 200

    def test_portal_dir(self, win_api):
        resp = win_api.portal_dir()
        assert resp.status_code == 200

    def test_download_pc_client(self, win_api):
        resp = win_api.download_pc_client()
        assert resp.status_code == 200

    def test_download_server_client(self, win_api):
        resp = win_api.download_server_client()
        assert resp.status_code == 200


class TestWinOther:
    """其他接口冒烟（2个）"""

    def test_get_task_detail_not_found(self, win_api):
        resp = win_api.get_task_detail("nonexistent", 999999)
        assert resp.status_code == 200
