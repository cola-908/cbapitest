"""
L3 集成/异常/边界测试
- Overview 数据一致性
- 4个模块并发可达
- 异常参数
"""

import pytest
import logging
import concurrent.futures

pytestmark = pytest.mark.integration
logger = logging.getLogger("cb-api-test")


class TestOverviewDataConsistency:
    """检验4个Overview接口返回数据结构一致性"""

    def test_four_overviews_all_ok(self, win_api, file_api, vmware_api, hyperv_api):
        """4个模块的overview都返回成功"""
        results = {
            "PC/Server": win_api.overview(),
            "FileServer": file_api.overview(),
            "VMware": vmware_api.overview(),
            "Hyper-V": hyperv_api.overview(),
        }
        for name, resp in results.items():
            assert resp.ok, f"{name} overview failed: {resp.message}"
            logger.info(f"{name} overview: devices={len(resp.data.get('device', resp.data.get('hosts', [])))}")

    def test_overview_has_expected_keys(self, win_api):
        """PC/Server overview 包含所有预期字段"""
        keys = ["device", "tasks", "versions", "log"]
        resp = win_api.overview()
        assert resp.ok
        for key in keys:
            assert key in resp.data, f"Missing key: {key}"


class TestConcurrentAccess:
    """4个后端并发可达性测试"""

    def test_all_modules_concurrent_health(self, tos_client):
        """并发请求4个后端，全部200"""
        results = tos_client.health_check()
        for name, ok in results.items():
            assert ok, f"{name} backend unreachable"


class TestEdgeCases:
    """边界/异常场景"""

    def test_win_task_with_large_id(self, win_api):
        resp = win_api.get_task(999999999)
        assert resp.status_code == 200

    def test_file_version_delete_nonexistent(self, file_api):
        resp = file_api.delete_version(999999)
        assert resp.status_code == 200

    def test_vmware_datacenters_nonexistent_device(self, vmware_api):
        resp = vmware_api.list_datacenters(999999)
        assert resp.status_code == 200

    def test_hyperv_device_not_found(self, hyperv_api):
        resp = hyperv_api.get_device("0.0.0.0")
        assert resp.status_code == 200

    def test_tos_volume_list_structure(self, tos_api):
        resp = tos_api.list_volumes()
        assert resp.ok
        if isinstance(resp.data, list):
            for vol in resp.data:
                assert "name" in vol or "volume" in str(vol).lower()


class TestDeepRoutes:
    """4-5层嵌套路由可达性"""

    def test_win_5_level_route(self, win_api):
        """最深层路由 /devices/{id}/tasks/{id}/versions/{vid}/disks/{did}/partitions/{pid}"""
        resp = win_api.get_disk_partitions("none", 0, "none", "none", "none")
        assert resp.status_code == 200

    def test_hyperv_3_level_task_route(self, hyperv_api):
        """3层任务路由 /tasks/{id}/{vid}/{sub}"""
        resp = hyperv_api.get_task_version_detail("none", "none", "none")
        assert resp.status_code == 200
