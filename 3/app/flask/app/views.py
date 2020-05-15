from app import app
from app.utils import * 

@app.route('/health', methods=['GET'])
def health_check():
  return redis_healthcheck()

@app.route('/add_word/<section>', methods=['GET'])
def add_word(section):
  if validate_input(section, "word"):
    word = section.split("=")[1]
    return redis_add_word(word)
  else:
    return "API Usage is /add_word/word=<your word>"

@app.route('/autocomplete/<section>', methods=['GET'])
def autocomplete(section):
  if validate_input(section, "query"):
    query = section.split("=")[1]
    return redis_autocomplete_word(query)
  else:
    return "API Usage is /autocomplete/query=<your word>"
