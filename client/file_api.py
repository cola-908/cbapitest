"""
FileServer API - 覆盖41个测试用例

代理路径前缀 /file → /v2/proxy2/CentralizedBackup

用例覆盖:
- CB-019, CB-020: 查询设备
- CB-021: SMB添加设备
- CB-113: rsync普通模式添加设备
- CB-114: rsync加密模式添加设备
- CB-115: SMB编辑设备
- CB-116: rsync编辑设备
- CB-022: 删除设备
- CB-023: 读取设备备份源目录
- CB-024: 创建SMB增量备份任务
- CB-025: 创建SMB镜像备份任务
- CB-026: 创建SMB多版本备份任务
- CB-034: 创建rsync增量备份任务
- CB-035: 创建rsync镜像备份任务
- CB-036: 创建rsync多版本备份任务
- CB-027: 删除备份任务
- CB-028: 查询备份任务列表
- CB-029: 编辑SMB增量备份任务
- CB-030: 编辑SMB镜像备份任务
- CB-031: 编辑SMB多版本备份任务
- CB-117: 编辑rsync增量备份任务
- CB-118: 编辑rsync镜像备份任务
- CB-119: 编辑rsync多版本备份任务
- CB-032: 启动备份任务
- CB-033: 停止备份任务
- CB-037: 查询SMB版本
- CB-038: 查询rsync版本
- CB-039: 删除版本
- CB-040: 导入SMB备份数据
- CB-052: 导入rsync备份数据
- CB-041: 解锁版本
- CB-042: 锁定版本
- CB-043: 查询还原任务
- CB-044: 创建增量还原
- CB-045: 创建多版本还原
- CB-046: 创建镜像还原
- CB-047: 启动还原
- CB-048: 停止还原(特殊路径)
- CB-049: 删除还原
- CB-051: TOS创建文件夹
- CB-053: 概览
"""

from typing import Any, Optional
from client.base import TOSHttpClient, APIResponse


class FileAPI:
    """FileServer 文件备份还原 API"""

    def __init__(self, client: TOSHttpClient):
        self.client = client

    # ══════════════════════════════════════════════════════
    # 设备管理
    # ══════════════════════════════════════════════════════
    def list_devices(self, device_type: Optional[str] = None) -> APIResponse:
        """GET /file/FileServer/device?type={all|smb|rsync}
        覆盖: CB-019 (SMB查询), CB-020 (rsync查询带type=all)
        """
        params = {"type": device_type} if device_type else None
        return self.client.get("/file/FileServer/device", params=params)

    def add_smb_device(self, data: dict) -> APIResponse:
        """POST /file/FileServer/device  — SMB添加设备
        覆盖: CB-021
        """
        return self.client.post("/file/FileServer/device", json=data)

    def add_rsync_device(self, data: dict) -> APIResponse:
        """POST /file/FileServer/device  — rsync普通模式添加设备
        覆盖: CB-113
        """
        return self.client.post("/file/FileServer/device", json=data)

    def add_rsync_encrypted_device(self, data: dict) -> APIResponse:
        """POST /file/FileServer/device  — rsync加密模式添加设备
        覆盖: CB-114
        """
        return self.client.post("/file/FileServer/device", json=data)

    def add_device(self, data: dict) -> APIResponse:
        """POST /file/FileServer/device
        覆盖: CB-021, CB-113, CB-114
        """
        return self.client.post("/file/FileServer/device", json=data)

    def edit_smb_device(self, data: dict) -> APIResponse:
        """PUT /file/FileServer/device  — SMB编辑设备
        覆盖: CB-115
        """
        return self.client.put("/file/FileServer/device", json=data)

    def edit_rsync_device(self, data: dict) -> APIResponse:
        """PUT /file/FileServer/device  — rsync编辑设备
        覆盖: CB-116
        """
        return self.client.put("/file/FileServer/device", json=data)

    def edit_device(self, data: dict) -> APIResponse:
        """PUT /file/FileServer/device
        覆盖: CB-115, CB-116
        """
        return self.client.put("/file/FileServer/device", json=data)

    def delete_device(self, device_id: str | int, data: Optional[dict] = None) -> APIResponse:
        """DELETE /file/FileServer/device/{device_id}
        覆盖: CB-022
        """
        return self.client.delete(f"/file/FileServer/device/{device_id}", json=data)

    def read_dir(self, data: dict) -> APIResponse:
        """POST /file/FileServer/device/readDir
        覆盖: CB-023
        """
        return self.client.post("/file/FileServer/device/readDir", json=data)

    # ══════════════════════════════════════════════════════
    # 备份任务 — 查询/列表/删除
    # ══════════════════════════════════════════════════════
    def list_backup_tasks(self) -> APIResponse:
        """GET /file/FileServer/backup_task
        覆盖: CB-028
        """
        return self.client.get("/file/FileServer/backup_task")

    def delete_backup_task(self, task_id: str | int, data: Optional[dict] = None) -> APIResponse:
        """DELETE /file/FileServer/backup_task/{task_id}
        覆盖: CB-027
        """
        return self.client.delete(f"/file/FileServer/backup_task/{task_id}", json=data)

    # ── 创建SMB备份任务 ────────────────────────────────
    def add_backup_task(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task  — SMB增量备份
        覆盖: CB-024
        """
        return self.client.post("/file/FileServer/backup_task", json=data)

    def add_backup_task_mirror(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task  — SMB镜像备份
        覆盖: CB-025
        """
        return self.client.post("/file/FileServer/backup_task", json=data)

    def add_backup_task_multi_version(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task  — SMB多版本备份
        覆盖: CB-026
        """
        return self.client.post("/file/FileServer/backup_task", json=data)

    # ── 创建rsync备份任务 ──────────────────────────────
    def add_rsync_backup_task(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task  — rsync增量备份
        覆盖: CB-034
        """
        return self.client.post("/file/FileServer/backup_task", json=data)

    def add_rsync_backup_task_mirror(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task  — rsync镜像备份
        覆盖: CB-035
        """
        return self.client.post("/file/FileServer/backup_task", json=data)

    def add_rsync_backup_task_multi_version(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task  — rsync多版本备份
        覆盖: CB-036
        """
        return self.client.post("/file/FileServer/backup_task", json=data)

    # ── 编辑SMB备份任务 ────────────────────────────────
    def edit_backup_task(self, task_id: str | int, data: dict) -> APIResponse:
        """PUT /file/FileServer/backup_task/{task_id}  — SMB增量
        覆盖: CB-029
        """
        return self.client.put(f"/file/FileServer/backup_task/{task_id}", json=data)

    def edit_backup_task_mirror(self, task_id: str | int, data: dict) -> APIResponse:
        """PUT /file/FileServer/backup_task/{task_id}  — SMB镜像
        覆盖: CB-030
        """
        return self.client.put(f"/file/FileServer/backup_task/{task_id}", json=data)

    def edit_backup_task_multi_version(self, task_id: str | int, data: dict) -> APIResponse:
        """PUT /file/FileServer/backup_task/{task_id}  — SMB多版本
        覆盖: CB-031
        """
        return self.client.put(f"/file/FileServer/backup_task/{task_id}", json=data)

    # ── 编辑rsync备份任务 ──────────────────────────────
    def edit_rsync_backup_task(self, task_id: str | int, data: dict) -> APIResponse:
        """PUT /file/FileServer/backup_task/{task_id}  — rsync增量
        覆盖: CB-117
        """
        return self.client.put(f"/file/FileServer/backup_task/{task_id}", json=data)

    def edit_rsync_backup_task_mirror(self, task_id: str | int, data: dict) -> APIResponse:
        """PUT /file/FileServer/backup_task/{task_id}  — rsync镜像
        覆盖: CB-118
        """
        return self.client.put(f"/file/FileServer/backup_task/{task_id}", json=data)

    def edit_rsync_backup_task_multi_version(self, task_id: str | int, data: dict) -> APIResponse:
        """PUT /file/FileServer/backup_task/{task_id}  — rsync多版本
        覆盖: CB-119
        """
        return self.client.put(f"/file/FileServer/backup_task/{task_id}", json=data)

    # ── 启动/停止备份 ──────────────────────────────────
    def start_backup_task(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/start
        覆盖: CB-032
        """
        return self.client.post("/file/FileServer/backup_task/start", json=data)

    def stop_backup_task(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/stop
        覆盖: CB-033
        """
        return self.client.post("/file/FileServer/backup_task/stop", json=data)

    # ══════════════════════════════════════════════════════
    # 版本管理
    # ══════════════════════════════════════════════════════
    def list_versions(self, task_id: str | int) -> APIResponse:
        """GET /file/FileServer/backup_task/versions/{task_id}
        覆盖: CB-037 (SMB版本查询)
        """
        return self.client.get(f"/file/FileServer/backup_task/versions/{task_id}")

    def list_versions_rsync(self, task_id: str | int) -> APIResponse:
        """GET /file/FileServer/backup_task/versions/{task_id}
        覆盖: CB-038 (rsync版本查询)
        """
        return self.client.get(f"/file/FileServer/backup_task/versions/{task_id}")

    def delete_version(self, data: dict) -> APIResponse:
        """DELETE /file/FileServer/backup_task/versions/delete
        覆盖: CB-039
        """
        return self.client.delete("/file/FileServer/backup_task/versions/delete", json=data)

    def lock_version(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/versions/lock
        覆盖: CB-042 (锁定版本)
        """
        return self.client.post("/file/FileServer/backup_task/versions/lock", json=data)

    def unlock_version(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/versions/lock
        覆盖: CB-041 (解锁版本)
        """
        return self.client.post("/file/FileServer/backup_task/versions/lock", json=data)

    # ══════════════════════════════════════════════════════
    # 导入备份数据
    # ══════════════════════════════════════════════════════
    def import_backup_smb(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/import  — SMB导入
        覆盖: CB-040
        """
        return self.client.post("/file/FileServer/backup_task/import", json=data)

    def import_backup_rsync(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/import  — rsync导入
        覆盖: CB-052
        """
        return self.client.post("/file/FileServer/backup_task/import", json=data)

    def import_backup(self, data: dict) -> APIResponse:
        """POST /file/FileServer/backup_task/import
        覆盖: CB-040, CB-052
        """
        return self.client.post("/file/FileServer/backup_task/import", json=data)

    # ══════════════════════════════════════════════════════
    # 还原任务
    # ══════════════════════════════════════════════════════
    def list_restore_tasks(self) -> APIResponse:
        """GET /file/FileServer/restore_task
        覆盖: CB-043
        """
        return self.client.get("/file/FileServer/restore_task")

    def add_restore_task(self, data: dict) -> APIResponse:
        """POST /file/FileServer/restore_task  — 创建增量还原
        覆盖: CB-044
        """
        return self.client.post("/file/FileServer/restore_task", json=data)

    def add_restore_task_multi_version(self, data: dict) -> APIResponse:
        """POST /file/FileServer/restore_task  — 创建多版本还原
        覆盖: CB-045
        """
        return self.client.post("/file/FileServer/restore_task", json=data)

    def add_restore_task_mirror(self, data: dict) -> APIResponse:
        """POST /file/FileServer/restore_task  — 创建镜像还原
        覆盖: CB-046
        """
        return self.client.post("/file/FileServer/restore_task", json=data)

    def start_restore_task(self, restore_id: str | int, data: Optional[dict] = None) -> APIResponse:
        """POST /file/FileServer/restore_task/{restore_id}/start
        覆盖: CB-047
        """
        return self.client.post(f"/file/FileServer/restore_task/{restore_id}/start", json=data)

    def stop_restore_task(self, restore_id: str | int) -> APIResponse:
        """POST /CentralizedBackup/FileServer/restore_task/{restore_id}/stop
        覆盖: CB-048  (特殊路径，不使用 /file 代理前缀)
        """
        return self.client.post(f"/CentralizedBackup/FileServer/restore_task/{restore_id}/stop")

    def delete_restore_task(self, restore_id: str | int, data: Optional[dict] = None) -> APIResponse:
        """DELETE /file/FileServer/restore_task/{restore_id}
        覆盖: CB-049
        """
        return self.client.delete(f"/file/FileServer/restore_task/{restore_id}", json=data)

    # ══════════════════════════════════════════════════════
    # TOS文件管理 (CB-051)
    # ══════════════════════════════════════════════════════
    def create_folder(self, data: dict) -> APIResponse:
        """POST /v2/fileManage/CreateFolder
        覆盖: CB-051 (TOS原生文件管理，不走代理)
        """
        return self.client.post("/v2/fileManage/CreateFolder", json=data)

    # ══════════════════════════════════════════════════════
    # 概览
    # ══════════════════════════════════════════════════════
    def overview(self) -> APIResponse:
        """GET /file/FileServer/overview
        覆盖: CB-053
        """
        return self.client.get("/file/FileServer/overview")
