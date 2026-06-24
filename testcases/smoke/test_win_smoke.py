"""
L1 冒烟测试 - PC/Server (Win) 模块
覆盖所有 21 个 API 用例 (CB-001 ~ CB-112)

每个用例至少一个测试方法，使用 pytest + win_api fixture。
"""

import pytest

pytestmark = pytest.mark.smoke


# ═══════════════════════════════════════════════════════
# 概览
# ═══════════════════════════════════════════════════════
class TestWinOverview:
    """概览 - CB-018"""

    def test_overview_ok(self, win_api):
        """CB-018: GET /win/overview"""
        resp = win_api.overview()
        assert resp.ok, f"overview failed: {resp.message}"
        assert isinstance(resp.data, dict)


# ═══════════════════════════════════════════════════════
# 设备管理
# ═══════════════════════════════════════════════════════
class TestWinDeviceList:
    """设备查询 - CB-001, CB-001b"""

    def test_list_devices_desktop(self, win_api):
        """CB-001: GET /win/devices?type=desktop"""
        resp = win_api.list_devices(device_type="desktop")
        assert resp.ok, f"list_devices(desktop) failed: {resp.message}"

    def test_list_devices_server(self, win_api):
        """CB-001b: GET /win/devices?type=server"""
        resp = win_api.list_devices(device_type="server")
        assert resp.ok, f"list_devices(server) failed: {resp.message}"


class TestWinDeviceDelete:
    """设备删除 - CB-002"""

    def test_delete_device_not_found(self, win_api):
        """CB-002: DELETE /win/devices/{device_id} — 不存在的设备"""
        resp = win_api.delete_device("00:00:00:00:00:00")
        assert resp.status_code == 200


class TestWinDeviceEdit:
    """设备编辑 - CB-105"""

    def test_edit_device(self, win_api):
        """CB-105: POST /win/devices/{device_id} 编辑设备"""
        resp = win_api.edit_device(
            "00:0c:29:59:f4:57",
            {"alias": "Computer-1dsddd"},
        )
        assert resp.status_code == 200


class TestWinDeviceVolumes:
    """卷信息 - CB-106"""

    def test_get_device_volumes(self, win_api):
        """CB-106: GET /win/devices/{device_id}/volumes"""
        resp = win_api.get_device_volumes("00:0c:29:59:f4:57")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 任务管理
# ═══════════════════════════════════════════════════════
class TestWinTaskList:
    """任务查询 - CB-003, CB-003b"""

    def test_list_tasks_desktop(self, win_api):
        """CB-003: GET /win/tasks?type=desktop"""
        resp = win_api.list_tasks(task_type="desktop")
        assert resp.ok, f"list_tasks(desktop) failed: {resp.message}"

    def test_list_tasks_server(self, win_api):
        """CB-003b: GET /win/tasks?type=server"""
        resp = win_api.list_tasks(task_type="server")
        assert resp.ok, f"list_tasks(server) failed: {resp.message}"


class TestWinRelink:
    """导入备份数据 - CB-004"""

    def test_relink_task(self, win_api):
        """CB-004: POST /win/tasks/relink"""
        resp = win_api.relink_task(
            data={"path": "/Volume1/public/CentralizedBackup"}
        )
        assert resp.status_code == 200


class TestWinBackupTaskCreate:
    """创建备份任务 - CB-005, CB-107, CB-108"""

    def test_create_full_device_backup(self, win_api):
        """CB-005: POST /win/devices/{device_id}/task — 整台设备备份"""
        resp = win_api.create_backup_task_full(
            "00:0c:29:59:f4:57",
            {
                "name": "Win-PC-Task-2",
                "device": "00:0c:29:59:f4:57",
                "type": 3,
                "dst_path": "/Volume1/public",
                "volumes": [""],
                "max_version": 2,
                "keep_all": True,
                "schedule_enable": True,
                "schedule": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "23",
                    "schedule_time": "2026-06-23",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 3,
                    "minute": 0,
                },
                "auto_awake": True,
                "sleep_avoid": True,
                "backup_external_disk": True,
            },
        )
        assert resp.status_code == 200

    def test_create_system_only_backup(self, win_api):
        """CB-107: POST /win/devices/{device_id}/task — 仅系统备份"""
        resp = win_api.create_backup_task_system(
            "00:0c:29:59:f4:57",
            {
                "name": "Win-PC-Task-3",
                "device": "00:0c:29:59:f4:57",
                "type": 2,
                "dst_path": "/Volume1/public",
                "volumes": [""],
                "max_version": 2,
                "keep_all": True,
                "schedule_enable": False,
                "schedule": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "23",
                    "schedule_time": "2026-06-23",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
                "auto_awake": True,
                "sleep_avoid": True,
                "backup_external_disk": True,
            },
        )
        assert resp.status_code == 200

    def test_create_custom_volume_backup(self, win_api):
        """CB-108: POST /win/devices/{device_id}/task — 自定义卷备份"""
        resp = win_api.create_backup_task_custom(
            "00:0c:29:59:f4:57",
            {
                "name": "Win-PC-Task-5",
                "device": "00:0c:29:59:f4:57",
                "type": 1,
                "dst_path": "/Volume1/public",
                "volumes": ["C"],
                "max_version": 2,
                "keep_all": True,
                "schedule_enable": False,
                "schedule": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "23",
                    "schedule_time": "2026-06-23",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
                "auto_awake": True,
                "sleep_avoid": True,
                "backup_external_disk": True,
            },
        )
        assert resp.status_code == 200


class TestWinTaskExec:
    """执行备份 - CB-006"""

    def test_exec_task_version(self, win_api):
        """CB-006: POST /win/devices/{device_id}/tasks/{task_id}/version"""
        resp = win_api.batch_exec_task(
            "00:0c:29:59:f4:57",
            11,
            data={},
        )
        assert resp.status_code == 200


class TestWinBatchCancel:
    """批量取消 - CB-007"""

    def test_batch_cancel_tasks(self, win_api):
        """CB-007: POST /win/batch/tasks/cancel"""
        resp = win_api.batch_cancel_tasks(
            data={
                "device_tasks": [
                    {"device_id": "00:0c:29:59:f4:57", "task_id": 7}
                ]
            }
        )
        assert resp.status_code == 200


class TestWinTaskDelete:
    """删除任务 - CB-008"""

    def test_delete_task(self, win_api):
        """CB-008: DELETE /win/devices/{device_id}/tasks/{task_id}"""
        resp = win_api.delete_task("00:0c:29:59:f4:57", 13)
        assert resp.status_code == 200


class TestWinBatchEdit:
    """批量编辑任务 - CB-009"""

    def test_batch_edit_task(self, win_api):
        """CB-009: POST /win/devices/{device_id}/tasks/{task_id}"""
        resp = win_api.batch_edit_task(
            "00:0c:29:59:f4:57",
            7,
            {
                "id": 7,
                "name": "Win-PC-Task-2",
                "dst_path": "/Volume1/public/CentralizedBackupImage/Windows/Win-PC-Task-2",
                "type": 3,
                "volumes": [""],
                "max_version": 2,
                "keep_all": True,
                "schedule_enable": True,
                "schedule": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "23",
                    "schedule_time": "2026-06-23",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 3,
                    "minute": 0,
                },
                "sleep_avoid": True,
                "auto_awake": True,
                "backup_external_disk": True,
            },
        )
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# Portal 浏览
# ═══════════════════════════════════════════════════════
class TestWinPortal:
    """Portal浏览 - CB-017"""

    def test_portal_dir(self, win_api):
        """CB-017: GET /win/portal/dir"""
        resp = win_api.portal_dir()
        assert resp.ok, f"portal_dir failed: {resp.message}"


# ═══════════════════════════════════════════════════════
# 版本管理
# ═══════════════════════════════════════════════════════
class TestWinVersionList:
    """版本查询 - CB-109"""

    def test_list_versions(self, win_api):
        """CB-109: GET /win/devices/{device_id}/tasks/{task_id}/versions"""
        resp = win_api.list_versions("00:0c:29:59:f4:57", 11)
        assert resp.status_code == 200


class TestWinVersionLock:
    """版本锁定/解锁 - CB-110, CB-111"""

    def test_lock_task_version(self, win_api):
        """CB-110: POST /win/devices/{device_id}/tasks/{task_id}/versions/{version_id} — 上锁"""
        resp = win_api.lock_task_version(
            "00:0c:29:59:f4:57",
            11,
            "2026-06-23_222953",
            data={"Locked": True},
        )
        assert resp.status_code == 200

    def test_unlock_task_version(self, win_api):
        """CB-111: POST /win/devices/{device_id}/tasks/{task_id}/versions/{version_id} — 解锁"""
        resp = win_api.unlock_task_version(
            "00:0c:29:59:f4:57",
            11,
            "2026-06-23_222953",
            data={"Locked": False},
        )
        assert resp.status_code == 200


class TestWinVersionDelete:
    """版本删除 - CB-112"""

    def test_delete_task_version(self, win_api):
        """CB-112: DELETE /win/devices/{device_id}/tasks/{task_id}/versions/{version_id}"""
        resp = win_api.delete_task_version(
            "00:0c:29:59:f4:57",
            11,
            "2026-06-23_222953",
            data={},
        )
        assert resp.status_code == 200
