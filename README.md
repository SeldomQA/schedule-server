# schedule-server

Scheduled task service based on APScheduler, You can dynamically add scheduled tasks.

## How to work

![](/image/schedule.png)

## Starting the service

* install 

```shell
> cd schedule_server
> pip install -r requirements.txt
```

* running

```shell
> python main.py

INFO:     Will watch for changes in these directories: ['/.../schedule-server/schedule_server']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [21905] using StatReload
INFO:     Started server process [21907]
INFO:     Waiting for application startup.
```

* api doc

url: http://127.0.0.1:8000/docs

![](/image/api_doc.png)


## How to use

__date__

* http://127.0.0.1:8000/scheduler/date/add_job

```json
{
  "job_id": "date_job_111",
  "url": "https://httpbin.org/get?id=1",
  "year": 2022,
  "month": 11,
  "day": 18,
  "hour": 7,
  "minute": 0,
  "second": 0
}
```

* job_id: 设置一个唯一的`job_id`，后面可以通过`job_id` 删除/暂停/恢复 定时任务。 
* url: 定时任务触发的url。
* datatime: 设置 `2022-11-18 07:00:00` 触发一次。这里用的是UTC时间，所以，北京时间你需要手动加8小时。


__interval__

* http://127.0.0.1:8000/scheduler/interval/add_job

```json
{
  "job_id": "interval_job_222",
  "url": "https://httpbin.org/get?id=2",
  "weeks": 0,
  "days": 0,
  "hours": 0,
  "minutes": 0,
  "seconds": 10
}
```

每次间隔 `10秒` 触发一次。

__crontab__

crontab的时间格式比较复杂，可以参考这个网站学习：

https://tooltt.com/crontab-parse/

* http://127.0.0.1:8000/scheduler/cron/add_job

```json
{
  "job_id": "cron_job_333",
  "url": "https://httpbin.org/get?id=3",
  "second": "0",
  "minute": "*/1",
  "hour": "*",
  "day": "*",
  "month": "*",
  "day_of_week": "*"
}
```
每次间隔 `1分钟` 触发一次。


__其他接口__

* 删除定时任务：`http://127.0.0.1:8000/scheduler/remove_job?job_id=interval_job_222`
* 暂停定时任务：`http://127.0.0.1:8000/scheduler/pause_job?job_id=interval_job_222`
* 恢复定时任务：`http://127.0.0.1:8000/scheduler/resume_job?job_id=interval_job_222`
