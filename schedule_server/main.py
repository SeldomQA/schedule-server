import requests
import uvicorn
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from utils.scheduler_conf import scheduler
from utils.redis_lock import lock
from utils.response import response
from utils.jobs import cron_job_data, date_job_data, interval_job_data, get_job_name
from api_schma import DateJob, IntervalJob, CronJob


app = FastAPI()


def scheduler_launch():
    """启动所有定时任务"""
    s = scheduler()
    s.start()
    print("start scheduler")


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


@lock("test_plan")
def requests_url(url):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {url}")
    r = requests.get(url)
    if r.status_code != 200:
        print(f"[Error] requests error. response\n:{r.text}", )


@app.post("/scheduler/date/add_job")
def scheduler_date_add_job(job: DateJob):
    """
    date 定时任务
    """
    s = scheduler()
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
    )
    s.start(paused=True)
    s.pause()

    return response(data={"job_id": job.id})


@app.post("/scheduler/cron/add_job")
def scheduler_cron_add_job(job: CronJob):
    """
    cron 定时任务
    """
    s = scheduler()
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
    )
    s.start(paused=True)
    s.pause()

    return response(data={"job_id": job.id})


@app.get("/scheduler/remove_job")
def scheduler_remove_job(job_id: str):
    """
    移除定时任务
    """
    s = scheduler()
    s.start()
    s.remove_job(job_id=job_id)
    return response()


@app.get("/scheduler/pause_job")
def scheduler_pause_job(job_id: str):
    """
    暂停定时任务
    """
    s = scheduler()
    s.start()
    s.pause_job(job_id=job_id)
    return response()


@app.get("/scheduler/resume_job")
def scheduler_resume_job(job_id: str):
    """
    恢复定时任务
    """
    s = scheduler()
    s.start()
    s.resume_job(job_id=job_id)
    return response()


@app.get("/scheduler/get_jobs")
def scheduler_resume_job(job_id: str = None):
    """
    查询定时任务列表
    """
    s = scheduler()
    s.start()
    jobs = []
    if job_id is not None:
        job = s.get_job(job_id=job_id)
        if job is not None:
            jobs.append(job)
    else:
        jobs = s.get_jobs()
    schedules = []
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

        schedules.append({
            "job_id": job.id,
            "name": job.name,
            "type": job_type,
            "data": job_data,
            "request_url": get_job_name(job),
            "next_run_time": job.next_run_time
        })

    tasks = {
        "task_list": schedules,
        "total": len(schedules)
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

    schedule = {
        "job_id": job.id,
        "name": job.name,
        "type": job_type,
        "data": job_data,
        "request_url": get_job_name(job),
        "next_run_time": job.next_run_time
    }

    return response(data=schedule)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
