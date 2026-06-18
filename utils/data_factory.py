"""
动态测试数据生成
"""

import time
import uuid


def unique_name(prefix: str = "test") -> str:
    """生成唯一名称: prefix_timestamp_uid"""
    ts = time.strftime("%m%d%H%M%S")
    uid = uuid.uuid4().hex[:4]
    return f"{prefix}-{ts}-{uid}"


def win_device_data(name: str = "", device_type: str = "desktop") -> dict:
    """PC/Server 设备数据"""
    return {
        "name": name or unique_name("win-pc"),
        "type": device_type,
    }


def file_smb_device_data(ip: str = "10.18.8.11", username: str = "admin", password: str = "") -> dict:
    """FileServer SMB 设备数据"""
    return {
        "name": unique_name("smb"),
        "ip": ip,
        "type": 0,  # SMB
        "username": username,
        "password": password,
    }


def file_rsync_device_data(ip: str = "10.18.8.11", username: str = "admin", password: str = "") -> dict:
    """FileServer Rsync 设备数据"""
    return {
        "name": unique_name("rsync"),
        "ip": ip,
        "type": 1,  # Rsync
        "username": username,
        "password": password,
    }


def vmware_device_data(ip: str, username: str = "root", password: str = "") -> dict:
    """VMware ESXi 设备数据"""
    return {
        "name": unique_name("vmware"),
        "ip": ip,
        "username": username,
        "password": password,
    }


def hyperv_device_data(ip: str, username: str = "administrator", password: str = "", port: int = 5985) -> dict:
    """Hyper-V 主机设备数据"""
    return {
        "host": ip,
        "user": username,
        "password": password,
        "port": port,
        "protocol": "http",
    }
