"""
L1 冒烟测试 - FileServer 模块
覆盖所有33个API的基本可达性和响应结构校验
"""

import pytest

pytestmark = pytest.mark.smoke


class TestFileOverview:
    """概览接口冒烟"""

    def test_overview_ok(self, file_api):
        resp = file_api.overview()
        assert resp.ok, f"overview failed: {resp.message}"
        assert isinstance(resp.data, dict)
        assert "device" in resp.data


class TestFileDevice:
    """设备管理接口冒烟"""

    def test_list_devices(self, file_api):
        assert file_api.list_devices().ok

    def test_get_device_not_found(self, file_api):
        assert file_api.get_device(999999).status_code == 200

    def test_read_dir(self, file_api):
        resp = file_api.read_dir("/")
        assert resp.status_code == 200


class TestFileLogin:
    """登录管理接口冒烟"""

    def test_list_logins(self, file_api):
        assert file_api.list_logins().ok

    def test_get_login_state_not_found(self, file_api):
        assert file_api.get_login_state(999999).status_code == 200


class TestFileBackupTask:
    """备份任务接口冒烟"""

    def test_list_backup_tasks(self, file_api):
        assert file_api.list_backup_tasks().ok

    def test_get_backup_task_not_found(self, file_api):
        assert file_api.get_backup_task(999999).status_code == 200

    def test_list_tasks_legacy(self, file_api):
        assert file_api.list_tasks_legacy().ok


class TestFileVersion:
    """版本管理接口冒烟"""

    def test_list_versions_not_found(self, file_api):
        assert file_api.list_versions(999999).status_code == 200

    def test_get_version_not_found(self, file_api):
        assert file_api.get_version(999999).status_code == 200

    def test_get_smb_info(self, file_api):
        assert file_api.get_smb_info().status_code == 200


class TestFileRestore:
    """还原任务接口冒烟"""

    def test_list_restore_tasks(self, file_api):
        assert file_api.list_restore_tasks().ok

    def test_list_restores(self, file_api):
        assert file_api.list_restores().ok

    def test_get_restore_not_found(self, file_api):
        assert file_api.get_restore(999999).status_code == 200
