from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger


def cron_job_data(job_trigger: CronTrigger) -> dict:
    """Returns data job data.
    :param job_trigger: CronTrigger object.
    return:
    """
    job_dict = {}
    for f in job_trigger.fields:
        job_dict[f.name] = str(f)
    return job_dict


def date_job_data(job_trigger: DateTrigger) -> dict:
    """Returns data job data.
    :param job_trigger: An apscheduler.job.Job instance.
    return:
    """
    datetime = job_trigger.__str__()[5:25]
    # 2023-10-01 00:00:00
    return {
        "year": int(datetime[0:4]),
        "month": int(datetime[5:7]),
        "day": int(datetime[8:10]),
        "hour": int(datetime[11:13]),
        "minute": int(datetime[14:16]),
        "second": int(datetime[17:19])
    }


def interval_job_data(job_trigger: IntervalTrigger) -> dict:
    """Returns data job data.
    :param job_trigger: An apscheduler.job.Job instance.
    return:
    """
    interval = job_trigger.__str__()[9:-1]
    if "day" in interval:
        # 暂不支持天以上的间隔
        return {}
    time_list = interval.split(":")
    '''
    val[0:00:01] 1s
    val[0:01:00] 1m
    val[1:00:00] 1h
    '''
    return {
        "hour": int(time_list[0]),
        "minute": int(time_list[1]),
        "second": int(time_list[2])
    }


def get_job_name(job) -> str:
    """Returns job name.
    :param job: An apscheduler.job.Job instance.
    :return: task name
    """
    return job.args[0]
