"""
author: bugmaster
date: 2022/11/12
Redis APScheduler
"""
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from config import SQLITE_PATH


def scheduler():
    """APScheduler: BackgroundScheduler"""

    jobstores = {
        # 默认使用 SQLite 数据库
        'default': SQLAlchemyJobStore(url=f'sqlite:///{SQLITE_PATH}')
    }

    executors = {
        'default': ThreadPoolExecutor(1),
        'processpool': ProcessPoolExecutor(1)
    }
    job_defaults = {
        'coalesce': True,  # 合并执行
        'max_instances': 1,    # 最大实例数为1
        'misfire_grace_time': 60  # 设置一个合理的misfire宽限时间
    }
    bs = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    return bs
