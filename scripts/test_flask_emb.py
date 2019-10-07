import requests
import json
data = ['asdf', 'asdf']
#url = "http://localhost:5000/api/emb/v1"
hostname= "localhost"
url = "http://{}:8500/api/emb/v1".format(hostname)
url = "http://{}:8500/api/emb/v2".format(hostname)
headers = {'content-type': 'application/json'}
resp = requests.post(url, json.dumps(data), headers=headers)
d = resp.json()
print(len(d), len(d[0]))
