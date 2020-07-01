from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import time
from pandas.tseries.offsets import Day
import requests
import math
import xmltodict
import os
import re
from threadpool import ThreadPool,makeRequests
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import threading
import datetime
import json

def main():
    keyword_list=[
        # '四季萌芽',
        # '小潮院长',
        # '虎牙寒冰大大'
        # '花花与三猫CatLive'
        '华农兄弟'
    ]
    pool = ThreadPool(5)
    param=[]
    base_url="https://search.bilibili.com/all?keyword={keyword}&from_source=nav_search_new"

    for word in keyword_list:
        param.append(([base_url,word],None))

    reqs = makeRequests(get_data,param)
    
    [pool.putRequest(req) for req in reqs] 
    #map(pool.putRequest,reqs)
    
    #wait(t, return_when=ALL_COMPLETED)
    pool.wait()
        
def get_data(base_url,word):
    base_url="https://search.bilibili.com/all?keyword={keyword}&from_source=nav_search_new"
    blt_p=[]
    blt_t=[]
    search_html=requests.get(base_url.format(keyword=word))
    uid=re.search(r'\/\/space.bilibili.com\/+(\d+)+\?',search_html.text,re.M|re.I).group(1)
    num=30
    vadio_list=[]
    vadio_obj=requests.get('https://api.bilibili.com/x/space/arc/search?mid={uid}&ps={num}&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'.format(uid=uid,num=num),data={},headers={
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://space.bilibili.com',
        'Referer': 'https://space.bilibili.com/10040906/video',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    })

    vadio_list.extend(vadio_obj.json()['data']['list']['vlist'])

    for i in range(math.ceil(vadio_obj.json()['data']['page']['count']/num)-1):
        vadio_obj=requests.get('https://api.bilibili.com/x/space/arc/search?mid={uid}&ps={num}&tid=0&pn={page}&keyword=&order=pubdate&jsonp=jsonp'.format(uid=uid,num=num,page=i+2),data={},headers={
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://space.bilibili.com',
            'Referer': 'https://space.bilibili.com/10040906/video',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
        })
        vadio_list.extend(vadio_obj.json()['data']['list']['vlist'])

    for vadio in vadio_list:
        aid=vadio['aid']
        oid_html=requests.get('https://www.bilibili.com/video/av{aid}'.format(aid=aid),data={},headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': """_uuid=758BB5EA-4745-FA8D-B317-FD9EB0F9159683204infoc; buvid3=78B61050-7726-483E-A2CB-A6C6CB980A24155807infoc; sid=bb6fece4; DedeUserID=62869140; DedeUserID__ckMd5=49de1e66c585f273; SESSDATA=2a25aa37%2C1579755236%2C65afe3c1; bili_jct=943986423e02e0dfa07c2ec0957df579; LIVE_BUVID=AUTO9115771632382651; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(umRk~~kuJY0J'ul~~uYJk~R; CURRENT_QUALITY=80; bp_t_offset_62869140=336483139725636343; INTVER=1""",
            'Host': 'www.bilibili.com',
            'Referer': 'https://space.bilibili.com/10040906/video',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
        })
        try:
            oid=re.search(r'"cid":(\d+),"', oid_html.text, re.M|re.I).group(1)
            bullet=requests.get('https://api.bilibili.com/x/v1/dm/list.so?oid={oid}'.format(oid=oid),data={},headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': """_uuid=758BB5EA-4745-FA8D-B317-FD9EB0F9159683204infoc; buvid3=78B61050-7726-483E-A2CB-A6C6CB980A24155807infoc; sid=bb6fece4; DedeUserID=62869140; DedeUserID__ckMd5=49de1e66c585f273; SESSDATA=2a25aa37%2C1579755236%2C65afe3c1; bili_jct=943986423e02e0dfa07c2ec0957df579; LIVE_BUVID=AUTO9115771632382651; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(umRk~~kuJY0J'ul~~uYJk~R; CURRENT_QUALITY=80; bp_t_offset_62869140=336483139725636343""",
            'Host': 'api.bilibili.com',
            'If-Modified-Since': 'Wed, 25 Dec 2019 17:53:49 GMT',
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/av38545246',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
        })
        except Exception as e:
            print(e,'oid报错')
            continue
        try:
            bullet_list=xmltodict.parse(bullet.content)['i']['d']
        except Exception as e:
            print(e,'弹幕报错')
            continue

        for blt in bullet_list:
            # 对弹幕作分析
            try:
                blt_p.append(blt['@p'])
            except Exception as e:
                print(e)
                blt_p.append('')
            try:
                blt_t.append(blt['#text'])
            except Exception as e:
                print(e)
                blt_t.append('')

    data=pd.DataFrame({'time':blt_p,'text':blt_t})
    data.to_csv('./bilibili/{name}.csv'.format(name=word),index=None)

if __name__ == "__main__":
    main()

