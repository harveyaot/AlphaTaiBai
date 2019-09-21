import requests
import json
data = ['asdf', 'asdf']
url = "http://localhost:5000/api/emb/v1"
headers = {'content-type': 'application/json'}
resp = requests.post(url, json.dumps(data), headers=headers)
d = resp.json()
print(len(d), len(d[0]))
