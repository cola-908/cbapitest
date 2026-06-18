"""
重试/轮询工具 - 用于备份等耗时任务的等待
"""

import time
import logging
from typing import Callable, Any

logger = logging.getLogger("cb-api-test")


def poll_until(
    func: Callable[[], Any],
    condition: Callable[[Any], bool],
    timeout: float = 120,
    interval: float = 5,
    description: str = "poll",
) -> Any:
    """
    轮询直到条件满足或超时

    Args:
        func: 获取状态的函数
        condition: 判断条件
        timeout: 超时秒数
        interval: 轮询间隔秒数
        description: 描述，用于日志

    Returns:
        最后一次 func 返回值

    Raises:
        TimeoutError: 超时未满足条件
    """
    start = time.time()
    while True:
        result = func()
        if condition(result):
            return result
        elapsed = time.time() - start
        if elapsed >= timeout:
            raise TimeoutError(f"{description} timed out after {timeout}s (last result: {result})")
        logger.debug(f"{description}: waiting... ({elapsed:.0f}s/{timeout}s)")
        time.sleep(interval)


def retry(
    func: Callable[[], Any],
    max_attempts: int = 3,
    delay: float = 1.0,
    description: str = "retry",
) -> Any:
    """
    重试执行函数

    Args:
        func: 要执行的函数
        max_attempts: 最大尝试次数
        delay: 每次重试间隔秒数
        description: 描述

    Returns:
        函数返回值

    Raises:
        最后一次异常
    """
    last_exception = None
    for i in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if i < max_attempts:
                logger.warning(f"{description}: attempt {i}/{max_attempts} failed: {e}, retrying...")
                time.sleep(delay)
    raise last_exception
