import json
import base64
import pymongo
import time
from json.encoder import JSONEncoder
from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)

azure_storage_account = None
mongo_connect = None
queue = "test"
queue = "general-image-2-crawl"
cookies = []
with open("local.settings.json") as fin:
    settings = json.load(fin)
    azure_storage_account = settings.get("AzureStorageAccount")
    mongo_connect = settings.get("MongoDBConnectionString")
    if not azure_storage_account or not mongo_connect:
        raise Exception("Null Settings on AzureStorageAccount or mongo connect")

# Setup Base64 encoding and decoding functions
base64_queue_client = QueueClient.from_connection_string(
                            conn_str=azure_storage_account, queue_name=queue,
                            message_encode_policy = BinaryBase64EncodePolicy(),
                            message_decode_policy = BinaryBase64DecodePolicy()
                        )

mongo_client =  pymongo.MongoClient(mongo_connect)
mongo_db = 'dev'
mongo_collection = "mingju5"
mongo_docs = mongo_client[mongo_db][mongo_collection]

with open("data/mingju.csv", 'r', encoding='utf-8') as fin:
    fin.readline()
    for idx, line in enumerate(fin):
        if idx < 2416:
            continue
        gs = line.split(",")
        assert len(gs) == 4
        doc = mongo_docs.find_one({"url":gs[1]})
        if doc and 'sent_baidu_img_res' in doc and doc['sent_baidu_img_res'] and 'data' in doc['sent_baidu_img_res'] and doc['sent_baidu_img_res']['data']:
            for i, image_info in enumerate(doc['sent_baidu_img_res']['data']):
                d_int, d_str = {}, {}
                if 'thumbURL' not in image_info:
                    continue
                for key, value in image_info.items():
                    if value:
                        if type(value) is int:
                            d_int[key] = value
                        if type(value) is str:
                            d_str[key] = value
                    d_str["source_mingju"] = gs[0]
                    d_str["source_mingju_url"] = gs[1]
                    d_str["source_mingju_author_title"] = gs[2]
                    d_str["source_mingju_poem_url"] = gs[3]

                    d_int['bdDisplayNum'] = doc['sent_baidu_img_res'].get('displayNum', 0)
                    d = {
                        "image_url" : image_info['thumbURL'], 
                        "add_string_info" : d_str,
                        "add_int_info" : d_int
                    }
                base64_queue_client.send_message(JSONEncoder().encode(d).encode('utf-8'))
        if doc:
            doc['crawled'] = int(time.time())
            mongo_docs.update_one({'url':gs[1]}, {"$set":doc})
            print(idx, gs[0], "Done")