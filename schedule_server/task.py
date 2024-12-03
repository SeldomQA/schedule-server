import requests
from utils.redis_lock import lock
from datetime import datetime
from loguru import logger


@lock("test_plan")
def requests_url(url):
    """
    requests task
    :param url:
    :return:
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"[{now}] {url}")
    r = requests.get(url)
    if r.status_code != 200:
        logger.error(f"requests error. response\n:{r.text}", )

