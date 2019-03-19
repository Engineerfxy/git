#导入模块   (只是对新华网的图片模块进行的保存)
import requests
import json
import re
import time
import csv
import threading
import random
from queue import Queue
from lxml import etree

#解析网页
def getUrl(gurl):
    USER_AGENT = random.choice([
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"
    ])
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(gurl,headers=headers)
    html = resp.text
    return html

#解析json格式
def getJson(url):
    html = getUrl(url)
    # print(html)
    # 转化为json 数据
    r = '[{].*[}]'
    htmlover = re.findall(r, html)
    # print(htmlover)
    parseJson = json.loads(htmlover[0])['data']['list']
    with open('新华图片.csv', 'a', encoding='utf-8', newline='') as f:
        write = csv.writer(f)
        write.writerow(['phTime(照片时间)', 'phLinkUrl(网页地址)', 'phUrl(图片链接)'])
        for parseonly in parseJson:
            pubtime = parseonly['PubTime']
            linkurl = parseonly['LinkUrl']
            imgarray = parseonly['imgarray']
            for eachimg in imgarray:
                write.writerow([pubtime,linkurl,eachimg])
        # print(parseonly)




#主运行程序
url = 'http://qc.wa.news.cn/nodeart/list?nid=115481&pgnum={}&cnt=20&tp=1&orderby=0?callback=jQuery17107545974516163052_1551670349563&_='
num = str(int(time.time()))
newurl = url + num
for i in range(1,50):
    urlOver = newurl.format(i)
    print(urlOver)
    getJson(urlOver)
    time.sleep(1)

# url= 'http://qc.wa.news.cn/nodeart/list?nid=115481&pgnum=2&cnt=20&tp=1&orderby=0?callback=jQuery17107545974516163052_1551670349563&_=1551678631'
# getJson(url)
# time.sleep(1)