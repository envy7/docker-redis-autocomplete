from app import app, redis_db
from redis import ConnectionError
from flask import jsonify
import re


def redis_healthcheck() -> bool:
    try:
        if redis_db.ping():
            return True
        else:
            return False
    except ConnectionError as err:
        app.logger.error(err)
        return False


def redis_add_word(word) -> bool:
    try:
        word = word.lower()
        for index in range(1, len(word)):
            redis_db.zadd(app.config['REDIS_ZSET'], {word[:index]: 0})

        word += '*'
        redis_db.zadd(app.config['REDIS_ZSET'], {word: 0})
        app.logger.info(f'Added the word {word[:-1]} to dictionary')
        return True
    except ConnectionError as err:
        app.logger.error(f'Failed adding word "{word}", to dictionary. {err}')
        return False


def redis_autocomplete_word(query):
    try:
        results = []
        response = {'words': results}
        batch_size = 50
        traverse = True

        query = query.lower()
        start = redis_db.zrank(app.config['REDIS_ZSET'], query)

        if not start:
            return(jsonify(response))

        app.logger.info(f'Fetching words for query {query} from position {start} in dictionary')
        while traverse:
            redis_range = redis_db.zrange(app.config['REDIS_ZSET'], start, start+batch_size-1)
            start += batch_size

            if not redis_range:
                break
            
            for entry in redis_range:
                minlen = min(len(entry), len(query))
                if entry[:minlen] != query[:minlen]:
                    traverse = False
                    break

                if entry[-1:] == '*':
                    results.append(entry[:-1])

        return(jsonify(response))
    except ConnectionError as err:
        app.logger.error(f'Failed autocomplete for query "{query}" in dictionary. {err}')
        return False


def validate_input(endpoint, action) -> bool:
    if re.match(rf"\b{action}\=([a-zA-Z]+)$", endpoint):
        return True
    else:
        return False
