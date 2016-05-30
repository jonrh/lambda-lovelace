
## Switch Keys Solution 30/05/2016

Today's work:
- Try to scan all the followers of @JOEdotie. It has more than 200,000 followers. Definitely, we have to switch keys to fetch such amount of data.


```python
import tweepy
import json
import pandas as pd
from collections import Counter
import datetime
from dateutil import parser
import math
from IPython.display import Image

token01 = {'consumer_key':'Bt7Ih6Bk5Y5kyLEUfbyyEwDjm',
           'consumer_secret':'x2vxVpEj0uK3ITXFgYLsncgvZEWi1nhnYbdB70GmsQMQ37Vgd6',
           'access_token':'711915268251983875-caR8pX1PJyW5g3aaZZXo9tNcSbXPev8',
           'access_secret':'DJKjqNuBmv7fUHVKDyuMmETeZHZ55IGqAmTuG0y0UysjZ'}

token02 = {'consumer_key':'WtxItBWIIw35Ei1tQ4Zrmkybk',
           'consumer_secret':'7KV0Mmg1P7qrIrYCeeRB5V1nKrVRK0r3PQiy7RwNWYTCDxNevH',
           'access_token':'734763903402553349-NkkB8v7VM27zGWtmB0F6JpP0ZKOzLGO',
           'access_secret':'nWq9x2e11PrJM676S1bwrT1OXwK5vLnvNCeOPJx6c5lEi'}

token03 = {'consumer_key':'vtuz2iuKhLujyBpr73MEXwfiX',
           'consumer_secret':'spYVh2VDjRpHtc2U6AANKmQRRBRibL5Aide5K2Qc5ZjuQBp5tk',
           'access_token':'734763903402553349-nT29dFC2dL3NnZxpzEYq9xw9izA3grs',
           'access_secret':'psTF8IdK7hVtRIhsQGkG7vagM6Lo5TIpCGaZM1w2wSWAm'}

token04 = {'consumer_key':'xag2EIHHObhGzFdIlpwPJZSUf',
           'consumer_secret':'YFclT3UB8m70OocWZG6d77DJRALzXaCHglA4KvS0O92RmyE5F3',
           'access_token':'734763903402553349-TnMxdWMmnUCdrpxJYsfwSxuT3U6cZ8C',
           'access_secret':'pt2uwcdX5GwBr46A1WfuUmFPG8MzhEL2OX9KXbPY2TPWV'}

token05 = {'consumer_key':'u4C5yqyz5IB5zca0QJ2IMV9zH',
           'consumer_secret':'8JLu7LeDrue9mzFNsgTJDgYL7cYH60n9vYc6AkmcNBHlyJsbJF',
           'access_token':'734763903402553349-dm7jGID00PTWTfF5s1ph1TiAFcb6WX0',
           'access_secret':'hYNTQEzqkYjX5oADpzoUGwWar7VdYlN35PQ5CR9pDnSC0'}

tokens = [token01,token02,token03,token04,token05]
```


```python
def auth(token):
    auth = tweepy.OAuthHandler(consumer_key = token['consumer_key'], consumer_secret = token['consumer_secret'])
    auth.set_access_token(token['access_token'], token['access_secret'])
    return tweepy.API(auth)
```

@JOEdotie has **264,900** followers.

15 * 5000 = 75000

264,800 / 75000 = 3.5

So we need 4 tokens


```python
total=[]
next_cursor = -1
i=0
api = auth(tokens[i])
while next_cursor != 0:
    try:
        followers_ids = api.followers_ids(screen_name='JOEdotie',count=5000,cursor=next_cursor)
        total = total + followers_ids[0]
        next_cursor = followers_ids[1][1]
        print(next_cursor)
    except tweepy.RateLimitError:
        i=i+1
        print(i)
        api = auth(tokens[i])#when hit the rate limit change to next key
```

    1534246837854489325
    1532652894441239334
    1531055144920832312
    1529434166244469560
    1527523356662853436
    1525927284178910697
    1524452465968892219
    1522654954980150522
    1520670554207749625
    1518829030181585359
    1516764246014407615
    1514682568299960348
    1512659287758511805
    1510478495167386426
    1
    1508032332701681099
    1506044886830186565
    1503689160723852819
    1501339388484359260
    1498882617619570248
    1496822403201780775
    1495035058016278012
    1493482205451204860
    1491934785307331709
    1490478582093808638
    1489036618647044145
    1487494609935788809
    1485483096249883004
    1483794291407330687
    1481975069901612861
    2
    1480230184638366993
    1478433860373256167
    1476310597879842438
    1474139285794860931
    1471694065993704768
    1468753235700809286
    1465660687626165706
    1462815607370592849
    1460334515482793726
    1458232040283260487
    1456618163514077916
    1454768843663417599
    1453900271649117457
    1450544430658527387
    1446510032756114346
    3
    1444828718877788921
    1441460581294659680
    1438654199774661602
    1435580882945374483
    1431063826500090030
    1425034550289992949
    1415582019839227700
    1400896153719219013
    0



```python
len(total)
```




    264928



Now compared to original 75,000 ids limit, we got 264,928 ids.

# Unfortunately...

### This approach againts the Twitter developer policy...which means we may risk on being blocked by twitter...

[Developer Policy](https://dev.twitter.com/overview/terms/policy):

Do not do any of the following:
- Use a single application API key for multiple use cases or **multiple application API keys for the same use case.**

I'm going to put the rate limit problem aside. Until we decide on how much tweets we exactly need.


```python

```
