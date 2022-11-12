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
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    bs = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    return bs
