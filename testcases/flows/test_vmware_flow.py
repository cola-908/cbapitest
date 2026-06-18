"""
L2 业务流测试 - VMware 备份还原链路
"""

import pytest
import logging

pytestmark = pytest.mark.flow
logger = logging.getLogger("cb-api-test")


class TestVMwareFlow:
    def test_overview(self, vmware_api):
        assert vmware_api.overview().ok

    def test_list_devices(self, vmware_api):
        assert vmware_api.list_devices().ok

    def test_list_tasks(self, vmware_api):
        assert vmware_api.list_tasks().ok

    def test_list_restore_tasks(self, vmware_api):
        assert vmware_api.list_restore_tasks().ok

    def test_get_task_devices(self, vmware_api):
        assert vmware_api.get_task_devices().status_code == 200
