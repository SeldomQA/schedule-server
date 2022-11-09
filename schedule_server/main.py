from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from scheduler import scheduler

app = FastAPI()


def say_hello(name):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now + f" Hello world, {name}")


class Item(BaseModel):
    seconds: int
    name: str


@app.post("/scheduler/interval/hello")
def scheduler_say_hello(item: Item):
    s = scheduler()
    s.add_job(say_hello, 'interval', seconds=item.seconds, args=[item.name])
    s.start()
    return {"/scheduler/interval/hello --> running!!"}


