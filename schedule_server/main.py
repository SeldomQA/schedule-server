from loguru import logger

import uvicorn
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.base import  JobLookupError
from utils.scheduler_conf import scheduler

from utils.response import response
from utils.jobs import cron_job_data, date_job_data, interval_job_data, get_job_name
from api_schma import DateJob, IntervalJob, CronJob
from task import requests_url

app = FastAPI()


def scheduler_launch():
    """启动所有定时任务"""
    s = scheduler()
    s.start()
    logger.info("start scheduler")


app.add_event_handler('startup', scheduler_launch)


# 跨域设置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/scheduler/date/add_job")
def scheduler_date_add_job(job: DateJob):
    """
    date 定时任务
    """
    s = scheduler()
    # 检查并删除已存在的任务
    try:
        existing_job = s.get_job(job.job_id)
        if existing_job:
            s.remove_job(job.job_id)
    except BaseException as msg:
        logger.error(msg)

    job = s.add_job(
        requests_url,
        'date',
        args=[job.url],
        id=job.job_id,
        max_instances=1,
        replace_existing=True,
        run_date=datetime(job.year, job.month, job.day, job.hour, job.minute, job.second),
    )
    s.start(paused=True)
    s.pause()

    return response(data={"job_id": job.id})


@app.post("/scheduler/interval/add_job")
def scheduler_interval_add_job(job: IntervalJob):
    """
    interval 定时任务
    """
    if job.hours is None and job.minutes is None and job.seconds is None:
        return response(error={"30001": "Please set the interval."})
    s = scheduler()
    
    # 检查并删除已存在的任务
    try:
        existing_job = s.get_job(job.job_id)
        if existing_job:
            s.remove_job(job.job_id)
    except BaseException as msg:
        logger.error(msg)
        
    job = s.add_job(
        requests_url,
        'interval',
        args=[job.url],
        id=job.job_id,
        max_instances=1,
        replace_existing=True,
        hours=job.hours,
        minutes=job.minutes,
        seconds=job.seconds,
        misfire_grace_time=None,  # 禁用misfire处理
        coalesce=True  # 合并错过的执行
    )

    return response(data={"job_id": job.id})


@app.post("/scheduler/cron/add_job")
def scheduler_cron_add_job(job: CronJob):
    """
    cron 定时任务
    """
    s = scheduler()
    # 检查并删除已存在的任务
    try:
        existing_job = s.get_job(job.job_id)
        if existing_job:
            s.remove_job(job.job_id)
    except BaseException as msg:
        logger.error(msg)

    # 确保second字段为'0'，避免每秒触发
    if job.second == '*':
        job.second = '0'
    
    job = s.add_job(
        requests_url,
        'cron',
        args=[job.url],
        id=job.job_id,
        max_instances=1,
        replace_existing=True,
        second=job.second,
        minute=job.minute,
        hour=job.hour,
        day=job.day,
        month=job.month,
        day_of_week=job.day_of_week,
        misfire_grace_time=60,
        coalesce=True
    )

    return response(data={"job_id": job.id})


@app.delete("/scheduler/remove_job")
def scheduler_remove_job(job_id: str):
    """
    移除定时任务
    """
    try:
        s = scheduler()
        s.start()
        s.remove_job(job_id=job_id)
    except JobLookupError:
        return response(success=False, error={"10010": "删除Job ID不存在"})
    return response()


@app.put("/scheduler/pause_job")
def scheduler_pause_job(job_id: str):
    """
    暂停定时任务
    """
    s = scheduler()
    s.start()
    try:
        s.pause_job(job_id=job_id)
    except JobLookupError:
        return response(success=False, error={"10011": "暂停Job ID不存在"})

    return response()


@app.put("/scheduler/resume_job")
def scheduler_resume_job(job_id: str):
    """
    恢复定时任务
    """
    s = scheduler()
    s.start()
    try:
        s.resume_job(job_id=job_id)
    except JobLookupError:
        return response(success=False, error={"10012": "恢复Job ID不存在"})
    return response()


@app.get("/scheduler/get_jobs")
def scheduler_resume_job(job_id: str = None):
    """
    查询定时任务列表
    """
    s = scheduler()
    s.start()
    jobs = s.get_jobs()
    schedules_condition = []
    schedules_all = []
    for job in jobs:
        job_type = None
        job_data = None
        if isinstance(job.trigger, CronTrigger):
            job_type = "cron"
            job_data = cron_job_data(job.trigger)
        elif isinstance(job.trigger, DateTrigger):
            job_type = "date"
            job_data = date_job_data(job.trigger)
        elif isinstance(job.trigger, IntervalTrigger):
            job_type = "interval"
            job_data = interval_job_data(job.trigger)

        status = "running" if job.next_run_time is not None else "paused"

        if job_id is not None and job_id in job.id:
            logger.info(f"condition - {job_id}, {job.id}")
            schedules_condition.append({
                "job_id": job.id,
                "name": job.name,
                "type": job_type,
                "data": job_data,
                "request_url": get_job_name(job),
                "next_run_time": job.next_run_time,
                "status": status
            })
        else:
            logger.info(f"condition - {job_id}, {job.id}")
            schedules_all.append({
                "job_id": job.id,
                "name": job.name,
                "type": job_type,
                "data": job_data,
                "request_url": get_job_name(job),
                "next_run_time": job.next_run_time,
                "status": status
            })

    if job_id is not None:
        tasks = {
            "task_list": schedules_condition,
            "total": len(schedules_condition)
        }
    else:
        tasks = {
            "task_list": schedules_all,
            "total": len(schedules_all)
        }

    return response(data=tasks)


@app.get("/scheduler/get_job")
def scheduler_resume_job(job_id: str):
    """
    查询某个定时任务
    """
    s = scheduler()
    s.start()
    job = s.get_job(job_id=job_id)

    job_type = None
    job_data = None
    if isinstance(job.trigger, CronTrigger):
        job_type = "cron"
        job_data = cron_job_data(job.trigger)
    elif isinstance(job.trigger, DateTrigger):
        job_type = "date"
        job_data = date_job_data(job.trigger)
    elif isinstance(job.trigger, IntervalTrigger):
        job_type = "interval"
        job_data = interval_job_data(job.trigger)

    status = "running" if job.next_run_time is not None else "paused"

    schedule = {
        "job_id": job.id,
        "name": job.name,
        "type": job_type,
        "data": job_data,
        "request_url": get_job_name(job),
        "next_run_time": job.next_run_time,
        "status": status
    }

    return response(data=schedule)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
