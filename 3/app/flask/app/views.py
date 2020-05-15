from app import app
from flask import jsonify
from app.utils import redis_healthcheck, redis_add_word, redis_autocomplete_word, validate_input


@app.route('/health', methods=['GET'])
def health_check():
    response = redis_healthcheck()
    if response:
        return 'Healthy'
    else:
        return 'Unhealthy'


@app.route('/add_word/<section>', methods=['GET'])
def add_word(section):
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
    if validate_input(section, 'query'):
        query = section.split('=')[1]
        response = redis_autocomplete_word(query)
        if response:
            return response, 200
        else:
            return 'Unable to autocomplete, please try again', 503
    else:
        return(jsonify({'error': 'API Usage is /autocomplete/query=<your word>'})), 400