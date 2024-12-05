"""
author: bugmaster
date: 2022/11/12
Redis redLock
"""
from time import sleep
import functools
from redlock import RedLock
from config import RedisCluster
from loguru import logger


def lock(key, expire_seconds=180, retry_times=3, retry_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_key = f"distributed_lock:{func.__name__}:{key}:{str(args)}"
            red_lock = RedLock(
                lock_key,
                connection_details=RedisCluster,
                ttl=expire_seconds * 1000,  # RedLock期望毫秒单位
                retry_times=retry_times,
                retry_delay=retry_delay * 1000  # RedLock期望毫秒单位
            )
            
            try:
                # 尝试获取锁
                if red_lock.acquire():
                    logger.debug(f"获取锁成功: {lock_key}")
                    try:
                        # 获取锁成功，执行函数
                        result = func(*args, **kwargs)
                        return result
                    finally:
                        # 确保函数执行完后释放锁
                        try:
                            red_lock.release()
                            logger.debug(f"释放锁: {lock_key}")
                        except:
                            logger.error(f"释放锁失败: {lock_key}")
                else:
                    logger.warning(f"获取锁失败，任务已在执行中: {lock_key}")
                    return None
            except Exception as e:
                logger.error(f"锁操作异常: {str(e)}")
                # 确保发生异常时也释放锁
                try:
                    red_lock.release()
                except BaseException as e:
                    raise e
                raise e

        return wrapper
    return decorator


@lock("unique_lock", expire_seconds=10)
def test():
    print("do something!!")
    sleep(2)


if __name__ == '__main__':
    test()
