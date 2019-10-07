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
    sent = '当爱已成往事'
    #url = "http://localhost:5000/api/emb/v1"
    hostname= "localhost"
    url = "http://{}:8600/api/sem_search/v1".format(hostname)
    headers = {'content-type': 'application/json'}
    resp = requests.post(url, json.dumps(sent), headers=headers)
    d = resp.json()
    print(d)

if __name__ == "__main__":
    test_search()
