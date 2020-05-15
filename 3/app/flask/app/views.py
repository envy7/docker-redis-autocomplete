from app import app
from flask import jsonify
from app.utils import redis_healthcheck, redis_add_word, redis_autocomplete_word, validate_input


@app.route('/health', methods=['GET'])
def health_check():
    """
    Route to do check health of application
    """

    response = redis_healthcheck()
    if response:
        return 'Healthy', 200
    else:
        return 'Unhealthy'. 503


@app.route('/add_word/<section>', methods=['GET'])
def add_word(section):
    """
    Route to add words to redis dictionary
    Call this API with passing a word to insert it into the redis dictionary
    Word can be any combination of english characters, lower and upper case
    ---
    parameters:
        - name: section (word=<your-word>)
          type: string
          required: true
          description: word to add to redis dictionary
    responses:
        200:
            description: Success fully added word to dictionary
        400:
            description: Invalid request format i.e not of form (/word=<your-word>)
        503:
            description: Issue with redis backend, word not added
    """

    if validate_input(section, 'word'):
        word = section.split('=')[1]
        response = redis_add_word(word)
        if response:
            return(jsonify({'success': 'word inserted to dictionary'})), 200
        else:
            return 'Word was not added successfully, please try again', 503
    else:
        return(jsonify({'error': 'API Usage is /add_word/word=<your word>'})), 400


@app.route('/autocomplete/<section>', methods=['GET'])
def autocomplete(section):
    """
    Route to get list of words from redis that start with given prefix
    Call this API with passing a prefix
    API can return either a json list of words or an empty list
    ---
    parameters:
        - name: section (query=<your-word>)
          type: string
          required: true
          description: prefix to query redis for autocompletion
    responses:
        - 200:
            description: Either empty list of words, or list of autocompleted words are returned
        - 400:
            description: Invalid request format i.e not of form (/query=<your-word>)
        - 503:
            description: Issue with redis backend, list of words not retrieved    
    """

    if validate_input(section, 'query'):
        query = section.split('=')[1]
        response = redis_autocomplete_word(query)
        if response:
            return response, 200
        else:
            return 'Unable to autocomplete, please try again', 503
    else:
        return(jsonify({'error': 'API Usage is /autocomplete/query=<your word>'})), 400
