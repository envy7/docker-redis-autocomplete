from os import environ


class Config:
    """Set configuration vars from env variables"""

    REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = environ.get('REDIS_PORT', 6379)
    REDIS_DATABASE = environ.get('REDIS_DATABASE', 0)
    REDIS_ZSET = environ.get('REDIS_ZSET', 'zset')
    REDIS_PASS = environ.get('REDIS_PASS')
    LOG_LEVEL = environ.get('LOG_LEVEL', 'INFO')
