import requests
from utils.redis_lock import lock
from datetime import datetime
from loguru import logger
import time


@lock("test_plan", expire_seconds=60)
def requests_url(url):
    """
    requests task
    :param url:
    :return:
    """
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{now}] {url}")
        r = requests.get(url)
        if r.status_code != 200:
            logger.error(f"requests error. response\n:{r.text}")
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
    finally:
        time.sleep(1)

