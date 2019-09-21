from flask import Flask
from flask import request
import json
from vector_es_search import *

app = Flask(__name__)

@app.route('/api/sem_search/v1', methods = ['POST'])
def sem_search():
    sent = request.json
    vec = get_vec4query(sent)
    resp = search_by_vec(vec)
    if resp.ok:
        return resp.json()
    else:
        return resp.text

if __name__ == "__main__":
    app.run()
