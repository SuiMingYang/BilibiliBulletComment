import pandas as pd
import jieba
from collections import Counter

data=pd.read_csv('./data/up_danmu/华农兄弟.csv')

data=data['text']
print(len(data))

res=[]
for i in data:
    try:
        # 去除停用词
        res.extend(jieba.lcut(i))
    except Exception as e:
        print(e)
        continue

word_freq=sorted(list(Counter(res).items()),key=lambda x:x[1],reverse=True)

for i in range(100):
    print(word_freq[i])

# #data=data['time'].str.extract(r'([\W\w]+)')[0].str.split(',').str[6]
# user_freq=sorted(list(Counter(data).items()),key=lambda x:x[1],reverse=True)
# for i in range(100):
#     print(user_freq[i])