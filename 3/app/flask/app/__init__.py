from app import views
from flask import Flask
from config import Config
import redis

app = Flask(__name__)
app.config.from_object(Config)
redis_db = redis.StrictRedis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DATABASE'],
    decode_responses=True
)
