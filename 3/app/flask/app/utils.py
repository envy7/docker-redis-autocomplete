from app import app, redis_db
from redis import ConnectionError
from flask import jsonify
import re

def redis_healthcheck():
  try:
    if redis_db.ping():
      return "Healthy"
    else:
      return "Unhealthy"
  except ConnectionError as err:
    app.logger.error(err)
    return "Unhealthy"

def redis_add_word(word):
  try:
    for index in range(1, len(word)):
      redis_db.zadd(app.config['REDIS_ZSET'], {word[:index]: 0})

    word += '*'
    redis_db.zadd(app.config['REDIS_ZSET'], {word: 0})
    return 'Successfully inserted word to dictionary'
  except ConnectionError as err:
    app.logger.error(err)
    return 'Word was not added successfully, please try again'

def redis_autocomplete_word(query):
  try:
    start = redis_db.zrank(app.config['REDIS_ZSET'], query)
    
    if not start:
      return(jsonify({}))

    redis_range = redis_db.zrange(app.config['REDIS_ZSET'], start, -1)
    results = []

    ## Todo: fetch entries in batches in a while loop
    for entry in redis_range:
      minlen = min(len(entry), len(query))
      if entry[:minlen] != query[:minlen]:
        break

      if entry[-1:] == '*':
        results.append(entry[:-1])

    return(jsonify({'words': results}))
  except:
    app.logger.error(err)
    return 'Unable to autocomplete, please try again'

def validate_input(endpoint, action):
  if re.match(rf"\b{action}\=([a-z]+)$", endpoint):
    return True
  else:
    return False
