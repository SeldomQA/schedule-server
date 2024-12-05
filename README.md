# schedule-server

Scheduled task service based on APScheduler, You can dynamically add scheduled tasks.

## How to work

![](/image/schedule.png)

* `schedule_server`: 核心功能是定时触发HTTP请求。
* `fontend`: 通过前端UI管理定时任务。
* `you server`: 你也可以通过调接口的方式管理定时任务。

## Starting the service

### schedule_server

* install 

```shell
> cd schedule_server
> pip install -r requirements.txt
```

* running

```shell
> uvicorn main:app --reload

INFO:     Will watch for changes in these directories: ['/.../schedule-server/schedule_server']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [21905] using StatReload
INFO:     Started server process [21907]
INFO:     Waiting for application startup.
```

__查看API__

访问url: http://127.0.0.1:8000/docs

![](/image/api_doc.png)


### frontend

* install 

```shell
> npm install
```

* running

```shell
> npm run dev

> wiremock-ui@0.0.1 dev
> vite
  VITE v4.3.9  ready in 3426 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

__查看UI__

访问url: http://localhost:5173/

![](/image/frontend.png)

## How to use

__date类型定时任务__

> 设置某一时间触发

* URL：http://127.0.0.1:8000/scheduler/date/add_job
* Method: `POST`

```json
{
  "job_id": "date_job_111",
  "url": "https://httpbin.org/get?id=111",
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


__interval类型定时任务__

> 设置间隔时间触发

* URL：http://127.0.0.1:8000/scheduler/interval/add_job
* Method: `POST`

```json
{
  "job_id": "interval_job_222",
  "url": "https://httpbin.org/get?id=222",
  "hours": 0,
  "minutes": 0,
  "seconds": 10
}
```

每次间隔 `10秒` 触发一次。

__crontab类型定时任务__

> crontab的时间格式比较复杂。
> 可以参考这个网站学习：https://tooltt.com/crontab-parse/


* URL：http://127.0.0.1:8000/scheduler/cron/add_job
* Method: `POST`

```json
{
  "job_id": "cron_job_333",
  "url": "https://httpbin.org/get?id=333",
  "second": "0",
  "minute": "*/3",
  "hour": "*",
  "day": "*",
  "month": "*",
  "day_of_week": "*"
}
```

每次间隔 `1分钟` 触发一次。


__其他接口__

* 删除定时任务：
  * URL:`http://127.0.0.1:8000/scheduler/remove_job?job_id=interval_job_222`
  * Method: `DELETE`

* 暂停定时任务：
  * `http://127.0.0.1:8000/scheduler/pause_job?job_id=interval_job_222`
  * Method: `PUT`

* 恢复定时任务：
  * URL：`http://127.0.0.1:8000/scheduler/resume_job?job_id=interval_job_222`
  * Method: `PUT`

* 查询定时任务：
  * URL：`http://127.0.0.1:8000/scheduler/get_job?job_id=interval_job_222`
  * Method：`GET`

* 查询所有定时任务：
  * URL：`http://127.0.0.1:8000/scheduler/get_jobs`
  * Method: `GET`
