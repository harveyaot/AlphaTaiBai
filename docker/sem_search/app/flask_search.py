import logging
from logging.config import fileConfig

from flask import Flask
from flask import request
import json
from vector_es_search import *

fileConfig('conf/logging_config.ini')
logger = logging.getLogger('search')

app = Flask(__name__)

@app.route('/api/sem_search/v1', methods = ['POST'])
def sem_search():
    sent = request.json
    vec = get_vec4query(sent)
    resp = search_by_vec(vec)
    if resp.ok:
        logger.info(log_request_record(sent, resp.json()))
        return resp.json()
    else:
        return resp.text

def log_request_record(sent, resp):
    resp = format_resp(resp)
    record = "\"{}\"\t{}".format(sent, resp)
    return record

def format_resp(resp):
    if resp and "hits" in resp and "hits" in resp['hits']:
        hits = resp['hits']['hits']
        res = []
        for hit in hits:
            sent = hit["_source"]["sent"]
            score = hit['_score']
            res.append("%s$%.2f" %(sent, score))
        return "|".join(res)
    else:
        return None

if __name__ == "__main__":
    app.run()
