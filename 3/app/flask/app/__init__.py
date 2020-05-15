from flask import Flask
from config import Config
from logging.config import dictConfig
import redis

LOGGING_CONFIG = { 
    'version': 1,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': { 
        '': {
            'handlers': ['default'],
            'level': 'INFO'
        }
    }
}
dictConfig(LOGGING_CONFIG)

app = Flask(__name__)
app.config.from_object(Config)
redis_db = redis.StrictRedis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DATABASE'],
    password=app.config['REDIS_PASS'],
    decode_responses=True
)

from app import views
