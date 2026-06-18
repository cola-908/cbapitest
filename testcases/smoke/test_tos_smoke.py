"""
L1 冒烟测试 - TOS System 模块
覆盖所有10个API的基本可达性
"""

import pytest

pytestmark = pytest.mark.smoke


class TestTOSLang:
    def test_get_lang(self, tos_api):
        resp = tos_api.get_lang()
        assert resp.ok


class TestTOSVersion:
    def test_get_app_version(self, tos_api):
        resp = tos_api.get_app_version()
        assert resp.ok

    def test_get_version_generic(self, tos_api):
        resp = tos_api.get_version_generic("CentralizedBackup")
        assert resp.ok


class TestTOSDesktop:
    def test_get_desktop_display(self, tos_api):
        resp = tos_api.get_desktop_display()
        assert resp.ok


class TestTOSFileManage:
    def test_get_home_list(self, tos_api):
        resp = tos_api.get_home_list()
        assert resp.ok

    def test_list_folders(self, tos_api):
        resp = tos_api.list_folders()
        assert resp.ok

    def test_get_folder_info_not_found(self, tos_api):
        resp = tos_api.get_folder_info("/nonexistent_path")
        assert resp.status_code == 200


class TestTOSStorage:
    def test_list_volumes(self, tos_api):
        resp = tos_api.list_volumes()
        assert resp.ok
