import requests
import json
headers = {'Content-Type': 'application/json'}
hostname = "loaclhost"
def creat_mapping(index_name):
    url = "http://{}:9200/".format(hostname) + index_name
    mapping = {
        "mappings": {
            "properties": {
                "bert-chinese-emb": {
                    "type": "dense_vector",
                    "dims": 768  
                },
                "sent":{
                    "type": "text"
                },
                "src":{
                    "type": "keyword",
                    "index": False
                },
                "author":{
                    "type": "keyword"
                },
                "title":{
                    "type": "text",
                    "fields":{
                        "keyword": {
                            "type" : "keyword",
                        }
                    }
                },
                "origin_src":{
                    "type":"keyword",
                    "index": False
                }
            }
        }
    }
    resp = requests.put(url, data=json.dumps(mapping), headers=headers)
    print(resp.text)

def index_sents_to_es(ds, index, batch_size=100):
    url = "http://{}:9200/{}/_bulk".format(hostname, index)
    step = int(len(ds) / batch_size) + 1
    for i in range(step):
        batch = ds[i*batch_size: (i+1)*batch_size]
        bulk = []
        for j, _ in enumerate(batch):
            _id = hash(batch[j]['title'] + batch[j]['sent'])
            pre = {'index':{ "_id": _id}}
            bulk.append(pre)
            bulk.append(batch[j])
        data = "\n".join([json.dumps(d) for d in bulk]) + '\n'
        print(i,len(batch))
        resp = requests.post(url, data=data, headers=headers)
    print(resp.text)

import hashlib
def hash(content):
    _str = hashlib.sha256(content.encode())
    return _str.hexdigest()[:20]

def read_sents(file_path):
    sents = []
    ds = []
    with open(file_path, encoding="utf-8") as fin:
        fin.readline()
        d = {}
        for line in fin:
            gs = line.strip('\r\n').split(',')
            sent, src, author_title, origin_src = gs[0:4]
            #print(author_title.split('《', 1))
            author, title = author_title.split('《', 1)
            title = "《" + title
            sents.append(gs[0])
            d = {
                "sent" : sent,
                "author": author,
                "title": title,
                "src": src,
                "origin_src": origin_src
            }
            ds.append(d)
    return sents, ds

def call_for_embs_and_index(sents, ds, batch_size):
    url = "http://{}:8500/api/emb/v1".format(hostname)
    step = int(len(sents) / batch_size) + 1
    for i in range(step):
        batch = sents[i*batch_size: (i+1)*batch_size]
        print(i,len(batch))
        print("calling {}".format(i))
        resp = requests.post(url, json.dumps(batch), headers=headers)
        d = resp.json()
        assert len(d) == len(batch)
        for j in range(len(d)):
            ds[j]['bert-chinese-emb'] = d[j]
        index_sents_to_es(ds[i*batch_size: (i+1)*batch_size], 'test_01')
    return ds

def index_sents(filepath):
    sents, ds = read_sents(filepath)
    ds = call_for_embs_and_index(sents[:], ds[:], 512)
    #index_sents_to_es(ds[:], "test_01")
    return ds

if __name__ == "__main__":
    creat_mapping("test_02")
    index_sents("../data/mingju.csv")
    #print(hash("adsf"))
