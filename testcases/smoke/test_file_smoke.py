"""
L1 冒烟测试 - FileServer 模块
覆盖所有 41 个 API 用例 (CB-019 ~ CB-053)

每个用例至少一个测试方法，使用 pytest + file_api fixture。
"""

import pytest

pytestmark = pytest.mark.smoke


# ═══════════════════════════════════════════════════════
# 概览
# ═══════════════════════════════════════════════════════
class TestFileOverview:
    """概览 - CB-053"""

    def test_overview_ok(self, file_api):
        """CB-053: GET /file/FileServer/overview"""
        resp = file_api.overview()
        assert resp.ok, f"overview failed: {resp.message}"
        assert isinstance(resp.data, dict)
        assert "device" in resp.data


# ═══════════════════════════════════════════════════════
# 设备管理 — 查询
# ═══════════════════════════════════════════════════════
class TestFileDeviceList:
    """设备查询 - CB-019, CB-020"""

    def test_list_devices(self, file_api):
        """CB-019: GET /file/FileServer/device — SMB查询设备"""
        resp = file_api.list_devices()
        assert resp.ok, f"list_devices failed: {resp.message}"

    def test_list_devices_all_types(self, file_api):
        """CB-020: GET /file/FileServer/device?type=all — rsync查询设备"""
        resp = file_api.list_devices(device_type="all")
        assert resp.ok, f"list_devices(type=all) failed: {resp.message}"


# ═══════════════════════════════════════════════════════
# 设备管理 — 添加
# ═══════════════════════════════════════════════════════
class TestFileDeviceAdd:
    """添加设备 - CB-021, CB-113, CB-114"""

    def test_add_smb_device(self, file_api):
        """CB-021: POST /file/FileServer/device — SMB添加设备"""
        resp = file_api.add_smb_device({
            "name": "SMB-Server-2",
            "port": 445,
            "type": 0,
            "ip": "10.18.8.155",
            "user": "demo",
            "password": "Admin123",
        })
        assert resp.status_code == 200

    def test_add_rsync_device(self, file_api):
        """CB-113: POST /file/FileServer/device — rsync普通模式添加设备"""
        resp = file_api.add_rsync_device({
            "name": "Rsync-Server-2",
            "port": 873,
            "type": 1,
            "rsync_mode": 2,
            "ip": "10.18.8.155",
            "user": "demo",
            "password": "Admin123",
        })
        assert resp.status_code == 200

    def test_add_rsync_encrypted_device(self, file_api):
        """CB-114: POST /file/FileServer/device — rsync加密模式添加设备"""
        resp = file_api.add_rsync_encrypted_device({
            "name": "Rsync-Server-2",
            "port": 9222,
            "type": 1,
            "rsync_mode": 1,
            "ip": "10.18.8.155",
            "user": "demo",
            "password": "Admin123",
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 设备管理 — 编辑
# ═══════════════════════════════════════════════════════
class TestFileDeviceEdit:
    """编辑设备 - CB-115, CB-116"""

    def test_edit_smb_device(self, file_api):
        """CB-115: PUT /file/FileServer/device — SMB编辑设备"""
        resp = file_api.edit_smb_device({
            "id": 4,
            "name": "SMB-Server-211",
            "createTime": 1782266932,
            "port": 445,
            "type": 0,
            "ip": "10.18.8.155",
            "user": "demo",
            "password": "Admin123",
        })
        assert resp.status_code == 200

    def test_edit_rsync_device(self, file_api):
        """CB-116: PUT /file/FileServer/device — rsync编辑设备"""
        resp = file_api.edit_rsync_device({
            "id": 5,
            "name": "Rsync-Server-211",
            "createTime": 1782267160,
            "port": 9222,
            "type": 1,
            "rsync_mode": 1,
            "ip": "10.18.8.155",
            "user": "demo",
            "password": "Admin123",
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 设备管理 — 删除 & 读取目录
# ═══════════════════════════════════════════════════════
class TestFileDeviceDelete:
    """删除设备 - CB-022"""

    def test_delete_device(self, file_api):
        """CB-022: DELETE /file/FileServer/device/{device_id}"""
        resp = file_api.delete_device(
            5,
            data={"device_ids": [4]},
        )
        assert resp.status_code == 200


class TestFileDeviceReadDir:
    """读取备份源目录 - CB-023"""

    def test_read_dir(self, file_api):
        """CB-023: POST /file/FileServer/device/readDir"""
        resp = file_api.read_dir({
            "path": "",
            "id": 4,
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 备份任务 — 创建 SMB
# ═══════════════════════════════════════════════════════
class TestFileBackupTaskCreateSMB:
    """创建SMB备份任务 - CB-024, CB-025, CB-026"""

    def test_add_backup_task_incremental(self, file_api):
        """CB-024: POST /file/FileServer/backup_task — SMB增量备份"""
        resp = file_api.add_backup_task({
            "destination": "/Volume1/public/z",
            "device_id": 4,
            "backup_mode": 0,
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "source": [{
                "root": "/demo",
                "selections": [{"selected": ".", "filtered": []}],
            }],
            "name": "SMB-Task-2",
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": False,
            "rsync_whole_file": False,
        })
        assert resp.status_code == 200

    def test_add_backup_task_mirror(self, file_api):
        """CB-025: POST /file/FileServer/backup_task — SMB镜像备份"""
        resp = file_api.add_backup_task_mirror({
            "destination": "/Volume1/public/j",
            "device_id": 4,
            "backup_mode": 1,
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "source": [{
                "root": "/demo",
                "selections": [{"selected": ".", "filtered": []}],
            }],
            "name": "SMB-Task-4",
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": False,
            "rsync_whole_file": False,
        })
        assert resp.status_code == 200

    def test_add_backup_task_multi_version(self, file_api):
        """CB-026: POST /file/FileServer/backup_task — SMB多版本备份"""
        resp = file_api.add_backup_task_multi_version({
            "destination": "/Volume1/public/d",
            "device_id": 4,
            "backup_mode": 2,
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "source": [{
                "root": "/demo",
                "selections": [{"selected": ".", "filtered": []}],
            }],
            "name": "SMB-Task-3",
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": False,
            "rsync_whole_file": False,
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 备份任务 — 创建 rsync
# ═══════════════════════════════════════════════════════
class TestFileBackupTaskCreateRsync:
    """创建rsync备份任务 - CB-034, CB-035, CB-036"""

    def test_add_rsync_backup_task_incremental(self, file_api):
        """CB-034: POST /file/FileServer/backup_task — rsync增量备份"""
        resp = file_api.add_rsync_backup_task({
            "destination": "/Volume1/public/zz",
            "device_id": 5,
            "backup_mode": 0,
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "source": [{
                "root": "/FFF",
                "selections": [
                    {"selected": "排序/名称排序", "filtered": []},
                    {"selected": "排序/图片格式", "filtered": []},
                ],
            }],
            "name": "Rsync-Task-2",
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": True,
            "rsync_whole_file": True,
        })
        assert resp.status_code == 200

    def test_add_rsync_backup_task_mirror(self, file_api):
        """CB-035: POST /file/FileServer/backup_task — rsync镜像备份"""
        resp = file_api.add_rsync_backup_task_mirror({
            "destination": "/Volume1/public/jj",
            "device_id": 5,
            "backup_mode": 1,
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "source": [{
                "root": "/FFF",
                "selections": [{"selected": "排序", "filtered": []}],
            }],
            "name": "Rsync-Task-3",
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": True,
            "rsync_whole_file": True,
        })
        assert resp.status_code == 200

    def test_add_rsync_backup_task_multi_version(self, file_api):
        """CB-036: POST /file/FileServer/backup_task — rsync多版本备份"""
        resp = file_api.add_rsync_backup_task_multi_version({
            "destination": "/Volume1/public/dd",
            "device_id": 5,
            "backup_mode": 2,
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "source": [{
                "root": "/FFF",
                "selections": [{
                    "selected": "排序",
                    "filtered": [
                        "排序/大小排序", "排序/时间排序", "排序/类型排序",
                        "排序/音频格式", "排序/默认排序",
                    ],
                }],
            }],
            "name": "Rsync-Task-4",
            "version_strategy": {"is_enabled": True, "max_num": 2},
            "rsync_compress": True,
            "rsync_whole_file": True,
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 备份任务 — 查询/删除/启停
# ═══════════════════════════════════════════════════════
class TestFileBackupTaskQuery:
    """查询备份任务列表 - CB-028"""

    def test_list_backup_tasks(self, file_api):
        """CB-028: GET /file/FileServer/backup_task"""
        resp = file_api.list_backup_tasks()
        assert resp.ok, f"list_backup_tasks failed: {resp.message}"


class TestFileBackupTaskDelete:
    """删除备份任务 - CB-027"""

    def test_delete_backup_task(self, file_api):
        """CB-027: DELETE /file/FileServer/backup_task/{task_id}"""
        resp = file_api.delete_backup_task(
            6,
            data={"ids": [6]},
        )
        assert resp.status_code == 200


class TestFileBackupTaskStartStop:
    """启动/停止备份 - CB-032, CB-033"""

    def test_start_backup_task(self, file_api):
        """CB-032: POST /file/FileServer/backup_task/start"""
        resp = file_api.start_backup_task(data={"ids": [9]})
        assert resp.status_code == 200

    def test_stop_backup_task(self, file_api):
        """CB-033: POST /file/FileServer/backup_task/stop"""
        resp = file_api.stop_backup_task(data={"ids": [6]})
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 备份任务 — 编辑 SMB
# ═══════════════════════════════════════════════════════
class TestFileBackupTaskEditSMB:
    """编辑SMB备份任务 - CB-029, CB-030, CB-031"""

    def test_edit_backup_task_incremental(self, file_api):
        """CB-029: PUT /file/FileServer/backup_task/{task_id} — SMB增量"""
        resp = file_api.edit_backup_task(6, {
            "id": 6,
            "name": "SMB-Task-2",
            "device_id": 4,
            "backup_mode": 0,
            "source": [{
                "root": "/demo",
                "selections": [{"selected": ".", "filtered": []}],
            }],
            "destination": "/Volume1/public/z",
            "scheduled_task": {
                "is_enabled": True,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 3,
                    "minute": 0,
                },
            },
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": False,
            "rsync_whole_file": False,
        })
        assert resp.status_code == 200

    def test_edit_backup_task_mirror(self, file_api):
        """CB-030: PUT /file/FileServer/backup_task/{task_id} — SMB镜像"""
        resp = file_api.edit_backup_task_mirror(4, {
            "id": 4,
            "name": "SMB-Task-4",
            "device_id": 4,
            "backup_mode": 1,
            "source": [{
                "root": "/demo",
                "selections": [{"selected": ".", "filtered": []}],
            }],
            "destination": "/Volume1/public/j",
            "scheduled_task": {
                "is_enabled": True,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": False,
            "rsync_whole_file": False,
        })
        assert resp.status_code == 200

    def test_edit_backup_task_multi_version(self, file_api):
        """CB-031: PUT /file/FileServer/backup_task/{task_id} — SMB多版本"""
        resp = file_api.edit_backup_task_multi_version(5, {
            "id": 5,
            "name": "SMB-Task-3",
            "device_id": 4,
            "backup_mode": 2,
            "source": [{
                "root": "/demo",
                "selections": [{"selected": ".", "filtered": []}],
            }],
            "destination": "/Volume1/public/d",
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "version_strategy": {"is_enabled": True, "max_num": 5},
            "rsync_compress": False,
            "rsync_whole_file": False,
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 备份任务 — 编辑 rsync
# ═══════════════════════════════════════════════════════
class TestFileBackupTaskEditRsync:
    """编辑rsync备份任务 - CB-117, CB-118, CB-119"""

    def test_edit_rsync_backup_task_incremental(self, file_api):
        """CB-117: PUT /file/FileServer/backup_task/{task_id} — rsync增量"""
        resp = file_api.edit_rsync_backup_task(7, {
            "id": 7,
            "name": "Rsync-Task-2",
            "device_id": 5,
            "backup_mode": 0,
            "source": [{
                "root": "/FFF",
                "selections": [
                    {"selected": "排序/名称排序", "filtered": []},
                    {"selected": "排序/图片格式", "filtered": []},
                ],
            }],
            "destination": "/Volume1/public/zz",
            "scheduled_task": {
                "is_enabled": True,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": True,
            "rsync_whole_file": True,
        })
        assert resp.status_code == 200

    def test_edit_rsync_backup_task_mirror(self, file_api):
        """CB-118: PUT /file/FileServer/backup_task/{task_id} — rsync镜像"""
        resp = file_api.edit_rsync_backup_task_mirror(8, {
            "id": 8,
            "name": "Rsync-Task-3",
            "device_id": 5,
            "backup_mode": 1,
            "source": [{
                "root": "/FFF",
                "selections": [{"selected": "排序", "filtered": []}],
            }],
            "destination": "/Volume1/public/jj",
            "scheduled_task": {
                "is_enabled": True,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "version_strategy": {"is_enabled": False, "max_num": 2},
            "rsync_compress": True,
            "rsync_whole_file": True,
        })
        assert resp.status_code == 200

    def test_edit_rsync_backup_task_multi_version(self, file_api):
        """CB-119: PUT /file/FileServer/backup_task/{task_id} — rsync多版本"""
        resp = file_api.edit_rsync_backup_task_multi_version(9, {
            "id": 9,
            "name": "Rsync-Task-4",
            "device_id": 5,
            "backup_mode": 2,
            "source": [{
                "root": "/FFF",
                "selections": [{
                    "selected": "排序",
                    "filtered": [
                        "排序/大小排序", "排序/时间排序", "排序/类型排序",
                        "排序/音频格式", "排序/默认排序",
                    ],
                }],
            }],
            "destination": "/Volume1/public/dd",
            "scheduled_task": {
                "is_enabled": False,
                "timed_task": {
                    "cycle_type": "EveryDay",
                    "cycle_weeks_range": "0,1,2,3,4,5,6",
                    "cycle_date": "24",
                    "schedule_time": "2026-06-24",
                    "frequency_type": "Disabled",
                    "frequency_value": 0,
                    "hour": 0,
                    "minute": 0,
                },
            },
            "version_strategy": {"is_enabled": True, "max_num": 5},
            "rsync_compress": True,
            "rsync_whole_file": True,
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 版本管理
# ═══════════════════════════════════════════════════════
class TestFileVersionList:
    """版本查询 - CB-037, CB-038"""

    def test_list_versions_smb(self, file_api):
        """CB-037: GET /file/FileServer/backup_task/versions/{task_id} — SMB版本"""
        resp = file_api.list_versions(2)
        assert resp.ok, f"list_versions(smb) failed: {resp.message}"

    def test_list_versions_rsync(self, file_api):
        """CB-038: GET /file/FileServer/backup_task/versions/{task_id} — rsync版本"""
        resp = file_api.list_versions_rsync(5)
        assert resp.ok, f"list_versions(rsync) failed: {resp.message}"


class TestFileVersionLock:
    """版本锁定/解锁 - CB-041, CB-042"""

    def test_unlock_version(self, file_api):
        """CB-041: POST /file/FileServer/backup_task/versions/lock — 解锁"""
        resp = file_api.unlock_version({
            "locked": False,
            "task_id": 5,
            "ver_id": 3,
        })
        assert resp.status_code == 200

    def test_lock_version(self, file_api):
        """CB-042: POST /file/FileServer/backup_task/versions/lock — 锁定"""
        resp = file_api.lock_version({
            "locked": True,
            "task_id": 5,
            "ver_id": 3,
        })
        assert resp.status_code == 200


class TestFileVersionDelete:
    """版本删除 - CB-039"""

    def test_delete_version(self, file_api):
        """CB-039: DELETE /file/FileServer/backup_task/versions/delete"""
        resp = file_api.delete_version({
            "task_id": 5,
            "ver_id": 4,
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 导入备份数据
# ═══════════════════════════════════════════════════════
class TestFileImport:
    """导入备份数据 - CB-040, CB-052"""

    def test_import_backup_smb(self, file_api):
        """CB-040: POST /file/FileServer/backup_task/import — SMB导入"""
        resp = file_api.import_backup_smb({
            "path": "/Volume1/public/CentralizedBackup",
            "device_type": 0,
        })
        assert resp.status_code == 200

    def test_import_backup_rsync(self, file_api):
        """CB-052: POST /file/FileServer/backup_task/import — rsync导入"""
        resp = file_api.import_backup_rsync({
            "path": "/Volume1/public/CentralizedBackup",
            "device_type": 1,
        })
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# 还原任务
# ═══════════════════════════════════════════════════════
class TestFileRestoreList:
    """查询还原任务 - CB-043"""

    def test_list_restore_tasks(self, file_api):
        """CB-043: GET /file/FileServer/restore_task"""
        resp = file_api.list_restore_tasks()
        assert resp.ok, f"list_restore_tasks failed: {resp.message}"


class TestFileRestoreCreate:
    """创建还原任务 - CB-044, CB-045, CB-046"""

    def test_add_restore_task_incremental(self, file_api):
        """CB-044: POST /file/FileServer/restore_task — 增量还原"""
        resp = file_api.add_restore_task({
            "name": "SMB-Task-2",
            "backup_task_id": 6,
            "source": [{
                "root": "/Volume1/public/z",
                "selections": [{"selected": "public/CentralizedBackup", "filtered": []}],
            }],
            "dest": "/FFF",
        })
        assert resp.status_code == 200

    def test_add_restore_task_multi_version(self, file_api):
        """CB-045: POST /file/FileServer/restore_task — 多版本还原"""
        resp = file_api.add_restore_task_multi_version({
            "name": "SMB-Task-3",
            "backup_task_id": 5,
            "source": [{
                "root": "/Volume1/public/d/2026-06-24_115353",
                "selections": [{"selected": "/.", "filtered": []}],
            }],
            "dest": "/FFF",
        })
        assert resp.status_code == 200

    def test_add_restore_task_mirror(self, file_api):
        """CB-046: POST /file/FileServer/restore_task — 镜像还原"""
        resp = file_api.add_restore_task_mirror({
            "name": "Rsync-Task-3",
            "backup_task_id": 8,
            "source": [{
                "root": "/Volume1/public/jj",
                "selections": [{"selected": "FFF/排序/大小排序", "filtered": []}],
            }],
            "dest": "/FFF",
        })
        assert resp.status_code == 200


class TestFileRestoreStartStop:
    """启动/停止还原 - CB-047, CB-048"""

    def test_start_restore_task(self, file_api):
        """CB-047: POST /file/FileServer/restore_task/{restore_id}/start"""
        resp = file_api.start_restore_task(3, data={})
        assert resp.status_code == 200

    def test_stop_restore_task(self, file_api):
        """CB-048: POST /CentralizedBackup/FileServer/restore_task/{restore_id}/stop — 特殊路径"""
        resp = file_api.stop_restore_task(3)
        assert resp.status_code == 200


class TestFileRestoreDelete:
    """删除还原任务 - CB-049"""

    def test_delete_restore_task(self, file_api):
        """CB-049: DELETE /file/FileServer/restore_task/{restore_id}"""
        resp = file_api.delete_restore_task(5, data={})
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════
# TOS 文件管理
# ═══════════════════════════════════════════════════════
class TestFileTOSFolder:
    """TOS创建文件夹 - CB-051"""

    def test_create_folder(self, file_api):
        """CB-051: POST /v2/fileManage/CreateFolder — TOS原生"""
        resp = file_api.create_folder({
            "path": "/Volume1/public/ee",
            "type": 2,
        })
        assert resp.status_code == 200
