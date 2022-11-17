from pydantic import BaseModel


class DateJob(BaseModel):
    job_id: str
    url: str
    year: int  # 4位数
    month: int  # 1~12
    day: int  # 1 - 31
    hour: int  # 0-23h
    minute: int  # 0 - 59m
    second: int  # 0 - 59s


class IntervalJob(BaseModel):
    job_id: str
    url: str
    weeks: int = None
    days: int = None
    hours: int = None
    minutes: int = None
    seconds: int = None


class CronJob(BaseModel):
    job_id: str
    url: str
    second: str = "*"  # 0 - 59s
    minute: str = "*"  # 0 - 59m
    hour: str = "*"  # 0-23h
    day: str = "*"  # 1 - 31
    month: str = "*"  # 1~12
    day_of_week: str = "*"  # 一周中的第几天(0 - 6) or (mon、tue、wed、thu、fri、fri、sat、sun)
