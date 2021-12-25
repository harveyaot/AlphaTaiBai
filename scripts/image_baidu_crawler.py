#encoding:utf-8

import requests
import pymongo
import json
import random
import time

from urllib import parse
from pymongo.common import raise_config_error
from urllib.parse import urlencode

# init readline from local configure
mongo_connect = None
cookies = []
with open("local.settings.json") as fin:
    settings = json.load(fin)
    mongo_connect = settings.get("MongoDBConnectionString")
    cookies = settings.get("Cookies")
    if not mongo_connect or not cookies:
        raise Exception("Null Settings on MongoDBConnectionString or cookies")

mongo_client =  pymongo.MongoClient(mongo_connect)
mongo_db = 'dev'
mongo_collection = "mingju5"
mongo_docs = mongo_client[mongo_db][mongo_collection]


def crawl_images_data(query):
    wd = {'word': query}
    qenc = urlencode(wd)

    url_base = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1640321085078_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&ctd=1640321085079%5E00_757X1002&sid=&"
    url = url_base + qenc

    headers = {
        'Connection' : 'keep-alive',
        'sec-ch-ua-mobile' : '?0',
        'sec-ch-ua-platform' : 'Windows',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
        'Sec-Fetch-Site' : 'same-origin',
        'Sec-Fetch-Mode' : 'navigate',
        'Sec-Fetch-User' : '?1',
        'Sec-Fetch-Dest' : 'document',
        'Referer' : url,
        'Accept-Language' : 'en,zh;q=0.9,zh-CN;q=0.8',
#        'Cookie' : 'BDqhfp=%E6%B1%9F%E4%B8%AD%E7%BB%BF%E9%9B%BE%E8%B5%B7%E5%87%89%E6%B3%A2%EF%BC%8C%E5%A4%A9%E4%B8%8A%E5%8F%A0%E5%B7%98%E7%BA%A2%E5%B5%AF%E5%B3%A8%26%260-10-1undefined%26%260%26%261; BIDUPSID=E2638723D8A4AAA82E8507B3F9F09FFC; PSTM=1625632220; BAIDUID=E2638723D8A4AAA8193E77945DD7B58E:FG=1; __yjs_duid=1_d6824d889d1f9780046ba4d4c57cb2991625807193880; BAIDUID_BFESS=E2638723D8A4AAA8193E77945DD7B58E:FG=1; __yjs_st=2_MGE5YTRkMTU2NTJiOGU5OWVhMGZjZjdiNjFkZDAwZTE3YjVhOTk3YWYzMjMzOGMzNDcwY2QyZGIwOTViYzlhMjJhNDZiMjI1MjgxMzVlMjQ0OWQ5NmE2NzJiNTU3M2NlMTY0YWRmYzYwN2U4ZmRhN2I1MmIyNDEwZGQ4N2U3YzBlMDE4MmI2ODIzZjA1MjRjNjIwMTg0N2MxOTNlZDQxY2Y3ZTU1MGNlZjZlYzZlMTUwYWU5ZmRlYjVmMjhiODkwNjFmYWQ0MzhjMDljMDdjN2U3MDZiNTYxNTZjYzE5MDIzZjgzMTM1YTM2MTNiMTAxMTBhZWM0NzNmZTc5YzI2YV83XzIxNDNmYWQ0; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; firstShowTip=1; cleanHistoryStatus=0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; indexPageSugList=%5B%22%E6%B1%9F%E4%B8%AD%E7%BB%BF%E9%9B%BE%E8%B5%B7%E5%87%89%E6%B3%A2%EF%BC%8C%E5%A4%A9%E4%B8%8A%E5%8F%A0%E5%B7%98%E7%BA%A2%E5%B5%AF%E5%B3%A8%22%2C%22%E7%BA%B5%E4%BD%BF%E6%96%87%E7%AB%A0%E6%83%8A%E6%B5%B7%E5%86%85%EF%BC%8C%E7%BA%B8%E4%B8%8A%E8%8B%8D%E7%94%9F%E8%80%8C%E5%B7%B2%22%2C%22%E5%A4%A9%E4%BD%95%E8%A8%80%E5%93%89%E4%B9%90%E6%97%A0%E7%A9%B7%EF%BC%8C%E5%B9%BF%E6%88%90%E5%BD%AD%E7%A5%96%E4%B8%BA%E4%B8%89%E5%85%AC%22%2C%22%E9%9A%8F%E9%A3%8E%E6%BD%9C%E5%85%A5%E5%A4%9C%EF%BC%8C%E6%B6%A6%E7%89%A9%E7%BB%86%E6%97%A0%E5%A3%B0%22%2C%22%E6%9A%82%E5%9B%A0%E8%8B%8D%E7%94%9F%E8%B5%B7%EF%BC%8C%E8%B0%88%E7%AC%91%E5%AE%89%E9%BB%8E%E5%85%83%22%2C%22%E8%8D%86%E7%8E%8B%E7%8C%8E%E6%97%B6%E9%80%A2%E6%9A%AE%E9%9B%A8%EF%BC%8C%E5%A4%9C%E5%8D%A7%E9%AB%98%E4%B8%98%E6%A2%A6%E7%A5%9E%E5%A5%B3%22%2C%22%E5%85%B6%E6%96%B0%E5%AD%94%E5%98%89%EF%BC%8C%E5%85%B6%E6%97%A7%E5%A6%82%E4%B9%8B%E4%BD%95%EF%BC%9F%22%2C%22%E6%AC%B2%E5%90%91%E9%98%B4%E5%85%B3%E5%BA%A6%EF%BC%8C%E9%98%B4%E5%85%B3%E6%99%93%E4%B8%8D%E5%BC%80%22%2C%22%E7%BE%8E%E4%BA%BA%E8%87%AA%E5%88%8E%E4%B9%8C%E6%B1%9F%E5%B2%B8%EF%BC%8C%E6%88%98%E7%81%AB%E6%9B%BE%E7%83%A7%E8%B5%A4%E5%A3%81%E5%B1%B1%22%5D; userFrom=null; ab_sr=1.0.1_MWZjZjAzY2FiMDJkYzAxMWU0ZDljY2QwY2FjMWU2ZWJlYTM0NDUxZTFlM2YzN2NmNGMwNGVjMTBjM2EyMDlkMjM4YTRhOWFlZmYxZWQyYzdiMGZiMTNjYWQ5YjVlMjRlYTRiNGRjZWFkNjNkYzU2MjhmM2I4MTMxYmIyNjg0ZDJkNjViNDQ4NzZiYzY5N2MxNGYwZGM1ODI4NWE0MDkzMQ=='
    }
    rnd_choice = random.choice(range(len(cookies)))
    print("Using Cookie", rnd_choice)
    if cookies[rnd_choice] != "":
        headers["Cookie"] = cookies[rnd_choice]
    resp = requests.get(url, headers=headers)
    t_line = None
    if resp.status_code == 200:
        text = resp.text
        for line in text.split("\n"):
            if "imgData" in line:
                t_line = line
    if t_line is None:
        raise Exception("Null http repsonse!")
    d = parse_image_data(t_line)
    return d

def parse_image_data(text):
    t_new = text.replace("app.setData('imgData',","").replace("'", "\"")
    return json.loads(t_new)

if __name__ ==  "__main__":
# read from mingju
    crawled = 0
    suc = 0
    with open("data/mingju.csv", 'r', encoding='utf-8') as fin:
        fin.readline()
        for idx, line in enumerate(fin):
            if idx < 9924:
                crawled += 1
                suc += 1
                continue
            gs = line.split(",")
            assert len(gs) == 4
            mingju = {
                "text" : gs[0],
                "url" : gs[1],
                "source":gs[2],
            }
            image_data = None
            crawled += 1
            if mongo_docs.find_one({"url":gs[1]}):
                suc += 1
                print(f'[Crawled {crawled}][Success:{suc}][Failure:{crawled-suc}]')
                continue
            try:
                image_data = crawl_images_data(mingju['text'])
            except Exception as e:
                print(e)

            if image_data is not None:
                suc += 1
                images = image_data['data']
                # pop the base64:
                for i, _ in enumerate(image_data['data']):
                    if 'base64' in image_data['data'][i]:
                        image_data['data'][i].pop('base64')
                mingju['sent_baidu_img_res'] = image_data
                mingju['sent_baidu_img_num'] =len(images)
                print(mingju['text'], len(images))
            else:
                mingju['sent_baidu_img_res'] = image_data
                mingju['sent_baidu_img_num'] = 0
            mongo_docs.insert_one(mingju)
            print(f'[Crawled {crawled}][Success:{suc}][Failure:{crawled-suc}]')
            rnd = random.random()
            time.sleep(rnd)