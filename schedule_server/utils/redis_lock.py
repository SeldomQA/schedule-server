"""
author: bugmaster
date: 2022/11/12
Redis redLock
"""
from time import sleep
import functools
from redlock import RedLock
from config import RedisCluster


def lock(key):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # If there is a lock, it is not executed
            red_lock = RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}",
                               connection_details=RedisCluster)
            if red_lock.acquire() is False:
                return func(*args, **kwargs)

        return wrapper

    return decorator


@lock("unique_lock")
def test():
    print("do something!!")
    sleep(2)


if __name__ == '__main__':
    test()
