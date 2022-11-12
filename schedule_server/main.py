import uvicorn
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from utils.scheduler_conf import scheduler
from utils.redis_lock import lock

app = FastAPI()


@lock("test_plan")
def say_hello(name):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now + f" Hello world, {name}")


class Item(BaseModel):
    seconds: int
    name: str


@app.get("/scheduler/launch")
def scheduler_launch():
    """
    启动所有定时任务
    :return:
    """
    s = scheduler()
    s.start()
    return {" --> A scheduled task has been started!!"}


@app.post("/scheduler/interval/hello")
def scheduler_say_hello(item: Item):
    """
    定时任务say_hello
    :param item:
    :return:
    """
    s = scheduler()
    s.add_job(say_hello, 'interval', seconds=item.seconds, args=[item.name])
    s.start(paused=True)
    s.pause()
    return {"/scheduler/interval/hello --> running!!"}


if __name__ == '__main__':
    uvicorn.run("main:app")
