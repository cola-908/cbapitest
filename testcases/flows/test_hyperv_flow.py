"""
L2 业务流测试 - Hyper-V 备份还原链路
"""

import pytest
import logging

pytestmark = pytest.mark.flow
logger = logging.getLogger("cb-api-test")


class TestHyperVFlow:
    def test_overview(self, hyperv_api):
        assert hyperv_api.overview().ok

    def test_list_devices(self, hyperv_api):
        assert hyperv_api.list_devices().ok

    def test_list_tasks(self, hyperv_api):
        assert hyperv_api.list_tasks().ok

    def test_list_restore_tasks(self, hyperv_api):
        assert hyperv_api.list_restore_tasks().ok
