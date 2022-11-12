import os

# SQLite path
SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs.sqlite")


class Config:
    # redis address
    RedisCluster = [{
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }]
