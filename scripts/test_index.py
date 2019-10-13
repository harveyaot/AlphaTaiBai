import requests
import json
headers = {'Content-Type': 'application/json'}
hostname = "loaclhost"
INDEX="test_01"
hostname = "mpgpu02.southcentralus.cloudapp.azure.com"
url = "http://{}:9200/test_01/_search?size=1000".format(hostname)

total , emb_count = 0, 0
resp = requests.get(url, headers=headers)
if resp.ok:
    res = resp.json()
    docs = res['hits']['hits']
    for doc in docs:
        if "bert-chinese-emb" in doc["_source"]:
            emb_count += 1
        total += 1
print(emb_count, total)
