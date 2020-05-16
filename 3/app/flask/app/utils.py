from app import app, redis_db
from redis import ConnectionError
from flask import jsonify
import re


def redis_healthcheck() -> bool:
    """
    Does a redis ping check to check redis connectivity, 
    if returns True, then application healthy to recieve requests
    ---
    parameters: None
    returns: 
        - bool
            description: Indicates if health check passed or not
    """

    try:
        if redis_db.ping():
            return True
        else:
            return False
    except ConnectionError as err:
        app.logger.error(err)
        return False


def redis_add_word(word) -> bool:
    """
    Adds words provided by user to redis zset if not already present
    Word is converted to lowercase, and added with a score of 0 to the zset
    Since all words are added with same score, the zset sorts them in lexicographic order
    All substrings of the word are extracted and added
    The complete word is added at the last with a '*' appended to it
    to distinguish it as the actual word added
    e.g for foo, entries added are f, fo, foo*
    ---
    parameters: 
        - name: word
        - type: string(anycase)
        - required: true
        - description: word to be parsed and added to redis zset
    returns:
        - bool:
            description: Indicates if word is added successfully or not
    """

    try:
        word = word.lower()
        if redis_db.zrank(app.config['REDIS_ZSET'], word):
            app.logger.info(f'Word "{word}" already present in dictionary')
            return True

        for index in range(1, len(word)):
            redis_db.zadd(app.config['REDIS_ZSET'], {word[:index]: 0})

        word += '*'
        redis_db.zadd(app.config['REDIS_ZSET'], {word: 0})
        app.logger.info(f'Added the word "{word[:-1]}" to dictionary')
        return True
    except ConnectionError as err:
        app.logger.error(f'Failed adding word "{word}", to dictionary. {err}')
        return False


def redis_autocomplete_word(query):
    """
    Finds words with matching prefix as the query
    Finds the start index by checking zrank of the given query, if zrank not found
    returns empty list. If zrank found starts searching for all words containing that prefix in batches from that point
    Batch size needs to be tweaked according to the mtu (i.e maximum data that can be retrieved from redis in one request)
    Search stops when the prefix and the words in zrange no longer match

    e.g in a zset with words foo, foobar and go added to it [f, fo, foo, foo*, foob, fooba, foobar*, g, go*] 
    if we need to find words with prefix fo
    search will start from fo and end at g, returning foo and foobar as possible results since they have * againts them
    ---
    parameters:
        - name: word
          type: string
          required: true
          description: prefix with which to search words in redis for autocomplete
    returns:
        - json:
            description: returns json list of words if found, or returns empty list
    """
    try:
        results = []
        response = {'words': results}
        batch_size = 50
        traverse = True

        query = query.lower()
        start = redis_db.zrank(app.config['REDIS_ZSET'], query)

        if not start:
            return(jsonify(response))

        app.logger.info(f'Fetching words for query "{query}" from position {start} in dictionary')
        while traverse:
            redis_range = redis_db.zrange(
                app.config['REDIS_ZSET'], start, start+batch_size-1)
            start += batch_size

            if not redis_range:
                break

            for entry in redis_range:
                minlen = min(len(entry), len(query))
                if entry[:minlen] != query[:minlen]:
                    traverse = False
                    break

                if entry[-1:] == '*' and entry[:-1] != query:
                    results.append(entry[:-1])

        return(jsonify(response))
    except ConnectionError as err:
        app.logger.error(
            f'Failed autocomplete for query "{query}" in dictionary. {err}')
        return False


def validate_input(endpoint, key) -> bool:
    """
    Validates whether input to the api is in correct format
    all endpoints have a key=value structure, key is either word/query
    value is a word consisting of any combination of letters of any case
    ---
    parameters:
        - name: endpoint
          type: string
          required: true
          description: The actual endpoint hit by the client which needs to validated
        - name: key
          type: string
          required: true
          description: The key being used in the api format
    returns:
        - bool:
            description: Indicates if the endpoint is of the proper format or not
    """


    if re.match(rf"\b{key}\=([a-zA-Z]+)$", endpoint):
        return True
    else:
        return False
