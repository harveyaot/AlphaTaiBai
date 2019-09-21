import requests
import json
url = "http://mpgpu02.southcentralus.cloudapp.azure.com:9200/test_01/_search"
headers = {'Content-Type': 'application/json'}
def search_by_vec(vec):
    d = {
        "_source" : ['sent', 'title', 'author'],
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.queryVector, doc['bert-chinese-emb'])",
                    "params": {
                    "queryVector": vec
                    }
                }
            }
        }
    }
    resp = requests.post(url, data=json.dumps(d),headers=headers)
    return resp

def get_vec4query(query):
    url = "http://mpgpu02.southcentralus.cloudapp.azure.com:8500/api/emb/v1"
    resp = requests.post(url, json.dumps([query]), headers=headers)
    d = resp.json()
    assert len(d) == 1
    return d[0]


if __name__ == "__main__":
    vec = get_vec4query("山有木兮木有枝，心悦君兮君不知。")
    res = search_by_vec(vec)
    print(res)
