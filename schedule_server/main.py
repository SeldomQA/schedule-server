import uvicorn
from datetime import datetime
from fastapi import FastAPI
from utils.scheduler_conf import scheduler
from utils.redis_lock import lock
from utils.response import response
from api_schma import Job

app = FastAPI()


def scheduler_launch():
    """启动所有定时任务"""
    s = scheduler()
    s.start()
    print("start scheduler")


app.add_event_handler('startup', scheduler_launch)


@lock("test_plan")
def say_hello(name):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now + f" Hello world, {name}")


@app.post("/scheduler/interval/add_job")
def scheduler_add_job(job: Job):
    """
    定时任务say_hello
    """
    s = scheduler()
    job = s.add_job(say_hello, 'interval', seconds=job.seconds, args=[job.name], id=job.job_id, replace_existing=True)
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
