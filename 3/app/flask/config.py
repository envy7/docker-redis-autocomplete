from os import environ


class Config:
    """Set configuration vars from env variables"""

    REDIS_HOST = environ.get('REDIS_HOST', default="localhost")
    REDIS_PORT = environ.get('REDIS_PORT', default=6379)
    REDIS_DATABASE = environ.get('REDIS_DATABASE', default=0)
    REDIS_ZSET = environ.get('REDIS_ZSET', default="zset")
    REDIS_PASS = environ.get('REDIS_PASS')
