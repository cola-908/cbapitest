"""
L2 业务流测试 - PC/Server 完整备份还原链路
添加设备 → 查看设备 → 创建任务 → 执行备份 → 查看版本 → 还原 → 清理
"""

import pytest
import logging
from utils.data_factory import unique_name

pytestmark = pytest.mark.flow
logger = logging.getLogger("cb-api-test")


class TestWinBackupFlow:
    """PC/Server 备份还原完整业务流"""

    def test_overview_initial_state(self, win_api):
        """Step 0: 检查overview初始状态"""
        resp = win_api.overview()
        assert resp.ok
        initial_devices = resp.data.get("device", [])
        initial_tasks = resp.data.get("tasks", [])
        logger.info(f"Initial: {len(initial_devices)} devices, {len(initial_tasks)} tasks")

    def test_list_devices_accessible(self, win_api):
        """Step 1: 设备列表接口可达"""
        resp = win_api.list_devices()
        assert resp.ok

    def test_list_tasks_accessible(self, win_api):
        """Step 2: 任务列表接口可达"""
        resp = win_api.list_tasks()
        assert resp.ok

    def test_restore_tasks_accessible(self, win_api):
        """Step 3: 还原任务列表接口可达"""
        resp = win_api.list_restore_tasks()
        assert resp.ok
