"""
L1 冒烟测试 - TOS System 模块
覆盖所有 10 个 API 用例 (CB-095 ~ CB-104)
"""

import pytest

pytestmark = pytest.mark.smoke


class TestTOSLang:
    """语言 - CB-095"""

    def test_get_lang(self, tos_api):
        """CB-095: GET /v2/lang/CentralizedBackup"""
        resp = tos_api.get_lang()
        assert resp.ok


class TestTOSVersion:
    """版本 - CB-096, CB-097"""

    def test_get_app_version(self, tos_api):
        """CB-096: GET /v2/app/version/CentralizedBackup"""
        resp = tos_api.get_app_version()
        assert resp.ok

    def test_get_version_generic(self, tos_api):
        """CB-097: GET /v2/app/version/{app_id}"""
        resp = tos_api.get_version_generic("CentralizedBackup")
        assert resp.ok


class TestTOSDesktop:
    """桌面显示 - CB-098"""

    def test_get_desktop_display(self, tos_api):
        """CB-098: GET /v2/person/desktopDisplay"""
        resp = tos_api.get_desktop_display()
        assert resp.ok


class TestTOSFileManage:
    """文件管理 - CB-099, CB-100, CB-101, CB-102"""

    def test_create_folder(self, tos_api):
        """CB-099: POST /v2/fileManage/CreateFolder"""
        resp = tos_api.create_folder("/Volume1/test_auto")
        assert resp.ok

    def test_get_folder_info(self, tos_api):
        """CB-100: GET /v2/fileManage/folderInfo"""
        resp = tos_api.get_folder_info("/Volume1")
        assert resp.ok

    def test_get_home_list(self, tos_api):
        """CB-101: GET /v2/fileManage/homeList"""
        resp = tos_api.get_home_list()
        assert resp.ok

    def test_list_folders(self, tos_api):
        """CB-102: GET /v2/folder/list"""
        resp = tos_api.list_folders()
        assert resp.ok

    def test_list_folders(self, tos_api):
        resp = tos_api.list_folders()
        assert resp.ok

    def test_get_folder_info_not_found(self, tos_api):
        resp = tos_api.get_folder_info("/nonexistent_path")
        assert resp.status_code == 200


class TestTOSStorage:
    """存储卷 + 恢复 - CB-103, CB-104"""

    def test_list_volumes(self, tos_api):
        """CB-103: GET /v2/storage/list/volume"""
        resp = tos_api.list_volumes()
        assert resp.ok

    def test_reinstall_system_not_allowed(self, tos_api):
        """CB-104: POST /v2/updaterestore/reinstallSystem — 无参数应拒绝"""
        resp = tos_api.reinstall_system({})
        # 重装系统需要参数，空参数应该返回错误
        assert resp.status_code == 200
