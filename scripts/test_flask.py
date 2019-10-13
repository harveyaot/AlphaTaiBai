import requests
import json
def test_emb():
    data = ['asdf', 'asdf']
    #url = "http://localhost:5000/api/emb/v1"
    hostname= "localhost"
    url = "http://{}:5000/api/emb/v1".format(hostname)
    headers = {'content-type': 'application/json'}
    resp = requests.post(url, json.dumps(data), headers=headers)
    d = resp.json()
    print(len(d), len(d[0]))

def test_search():
    sent = '计算机病毒'
    #url = "http://localhost:5000/api/emb/v1"
    hostname= "mpgpu02.southcentralus.cloudapp.azure.com"
    url = "http://{}:8600/api/sem_search/v2".format(hostname)
    headers = {'content-type': 'application/json'}
    resp = requests.post(url, json.dumps(sent), headers=headers)
    d = resp.json()
    record = log_request_record(sent, d)
    print(record)

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
            print(sent, float(score))
            res.append("%s$%.2f" %(sent, score))
        return "|".join(res)
    else:
        return None

if __name__ == "__main__":
    test_search()
