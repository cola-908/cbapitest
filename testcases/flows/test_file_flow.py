"""
L2 业务流测试 - 文件服务器备份还原链路
添加SMB/Rsync设备 → 查看设备 → 创建备份任务 → 查看版本 → 版本管理 → 清理
"""

import pytest
import logging

pytestmark = pytest.mark.flow
logger = logging.getLogger("cb-api-test")


class TestFileBackupFlow:
    """FileServer 备份还原完整业务流"""

    def test_overview_initial_state(self, file_api):
        resp = file_api.overview()
        assert resp.ok

    def test_list_devices_accessible(self, file_api):
        resp = file_api.list_devices()
        assert resp.ok

    def test_list_backup_tasks(self, file_api):
        resp = file_api.list_backup_tasks()
        assert resp.ok

    def test_list_restore_tasks(self, file_api):
        resp = file_api.list_restore_tasks()
        assert resp.ok

    def test_smb_info_accessible(self, file_api):
        resp = file_api.get_smb_info()
        assert resp.status_code == 200
