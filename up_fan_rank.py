import requests as reqs
import re
import numpy
import pandas as pd
import time

def stat(mode=''):
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    res=reqs.get('https://www.kanbilibili.com/rank/ups/{}'.format(mode))
    info=re.findall(r"""<a target="_blank" href="(.*?)" class="" data-reactid="(.*?)"><div class="up-item" data-reactid="(.*?)"><span class="index" data-reactid="(.*?)">(.*?)</span><img class="face" src="(.*?)@15Q" data-reactid="(.*?)"/><div class="basic" data-reactid="(.*?)"><span class="name blue" data-reactid="(.*?)">(.*?)</span><span class="gender gender-(\d)" data-reactid="(.*?)"></span><div class="sign" data-reactid="(.*?)">(.*?)</div></div><div class="info" data-reactid="(.*?)"><div class="change" data-reactid="(.*?)"><div class="icon (.*?)-change" data-reactid="(.*?)">(.*?)</div></div><div class="info-item" data-reactid="(.*?)"><p class="data fans" data-reactid="(.*?)">(.*?)</p><p class="label" data-reactid="(.*?)">粉丝数</p></div><div class="info-item" data-reactid="(.*?)"><p class="data playNum" data-reactid="(.*?)">(.*?)</p><p class="label" data-reactid="(.*?)">播放数</p></div></div></div></a>""",res.text.replace('\r','').replace('\n',''))

    index=[]
    name=[]
    face=[]
    gender=[]
    abstract=[]
    change=[]
    fans_count=[]
    play_count=[]
    space_url=[]

    for obj in info:
        index.append(obj[4])
        face.append(obj[5])
        name.append(obj[9])
        gender.append('1' if obj[10]=='1' else '0')
        abstract.append(obj[13])
        change.append(obj[17])
        fans_count.append(obj[21])
        play_count.append(obj[25])
        space_url.append(obj[1])

    data=pd.DataFrame({
        'index':index,
        'name':name,
        'change':change,
        'fans_count':fans_count,
        'play_count':play_count,
        'gender':gender,
        'abstract':abstract,
        'space_url':space_url,
        'face':face
    })

    data.to_csv('./data/{}/stat_{}_{}.csv'.format(mode,mode,t),index=None)
    print(mode,'success',t,len(data))
import time
if __name__ == "__main__":
    stat('playNum')