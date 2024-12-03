import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SQLite path
SQLITE_PATH = os.path.join(BASE_DIR, "jobs.sqlite")

# redis address
RedisCluster = [{
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}]
