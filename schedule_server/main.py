import requests
import uvicorn
from datetime import datetime
from fastapi import FastAPI
from utils.scheduler_conf import scheduler
from utils.redis_lock import lock
from utils.response import response
from api_schma import DateJob, IntervalJob, CronJob

app = FastAPI()


def scheduler_launch():
    """启动所有定时任务"""
    s = scheduler()
    s.start()
    print("start scheduler")


app.add_event_handler('startup', scheduler_launch)


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
    if job.weeks is None and job.days is None and job.hours is None and job.minutes is None and job.seconds is None:
        return response(error={"30001": "Please set the interval."})
    s = scheduler()
    job = s.add_job(
        requests_url,
        'interval',
        args=[job.url],
        id=job.job_id,
        max_instances=1,
        replace_existing=True,
        weeks=job.weeks,
        days=job.days,
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


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
