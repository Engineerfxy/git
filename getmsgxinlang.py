import requests
import json
import random
from queue import Queue
import re
import os
import threading
import time


#
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
#
# url ='https://interface.sina.cn/pc_api/public_news_da ta.d.json?callback=jQuery111207817713212374895_1551346046464&cids=260&type=std_news%2Cstd_video%2Cstd_slide&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hrfqzka9263530%2Chsxncvf8025355%2Chrfqzka9339537%2Chqfskcp7620000%2Chqfskcp7637563%2Chrfqzka9701884%2Chrfqzka9643390&mod=nt_home_fashion_latest&cTime=1548753601&action=0&_=1551402315'
# resp = requests.get(url,headers=headers)
#
# s = resp.text
# r ='[{].*[}]'
# sover = re.findall(r,s)
# print(sover)
# q = json.loads(sover)['data']
# print(q)

class xlSpider(object):
    def __init__(self):
        self.number = 0
        self.nowtime = int(time.time())
        self.filenames = ['新浪时尚','新浪科技','新浪汽车','新浪体育','新浪娱乐',]
        self.headers = random.choice([
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"
        ])
        #创建队列
        self.urlQueue = Queue()
        self.resQueue = Queue()

    #生成url 队列
    def getUrl(self):
        urllist = [
            #新浪时尚
            'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111207817713212374895_1551346046464&cids=260&type=std_news%2Cstd_video%2Cstd_slide&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=100&up=0&down=0&top_id=hrfqzka9263530%2Chsxncvf8025355%2Chrfqzka9339537%2Chqfskcp7620000%2Chqfskcp7637563%2Chrfqzka9701884%2Chrfqzka9643390&mod=nt_home_fashion_latest&cTime=1548753601&action=0&_=',
            #新浪汽车
            'https://cre.mix.sina.com.cn/api/v3/get?callback=jQuery111208568032614304597_1551345455623&cateid=1z&cre=tianyi&mod=pctech&merge=3&statics=1&length=100&up=0&down=0&tm=1551345455&action=0&top_id=BtmLm%2CBtmOX%2CBtmPg%2CBtewl%2CBtRAz%2CBu6aZ%2CBtcFa%2CBtzBz%2CBu2MR%2CBtnag%2CBu19p%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1551345455776%7D&_=',
            #新浪科技
            'https://cre.mix.sina.com.cn/api/v3/get?callback=jQuery111208568032614304597_1551345455623&cateid=1z&cre=tianyi&mod=pctech&merge=3&statics=1&length=100&up=0&down=0&tm=1551345455&action=0&top_id=BtmLm%2CBtmOX%2CBtmPg%2CBtewl%2CBtRAz%2CBu6aZ%2CBtcFa%2CBtzBz%2CBu2MR%2CBtnag%2CBu19p%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1551345455776%7D&_=',
            #新浪体育
            'http://cre.mix.sina.com.cn/api/v3/get?callback=jQuery11130956658864266061_1551339796876&cateid=2L&cre=tianyi&mod=pcspth&merge=3&statics=1&tm=1551339797&length=100&offset=0&action=0&up=0&top_id=089592e48dfb3a128236eb7d7afb7e49%2C089592e48dfb3a128236eb7d7afb7e49%2CBtmFY%2CBtmFY%2CBtaen%2CBtaen%2CBtOLu%2CBtOLu%2CBtOLu%2CBtOLu&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1551339796910+%7D&_=',
            #新浪娱乐
            'https://cre.mix.sina.com.cn/api/v3/get?callback=jQuery111205959530882862778_1551340672743&cateid=1Q&cre=tianyi&mod=pcent&merge=3&statics=1&length=100&up=0&down=0&tm=1551340672&action=0&top_id=BtoME%2CBu9SG%2CBtoME%2CBtUOj%2CBuJd8%2CBuGUS%2CBtnHB%2CBuCr3%2CBu4nY%2CBtrFO%2CBtVSd%2CBtVSd%2CBtPmc%2CBtEOI%2CBtWtd&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1551340672767%7D&_=',
        ]
        for pURL in  urllist:
            #拼接URL
            url = pURL + str(self.nowtime)
            # print(url)  没问题
            self.urlQueue.put(url)
            print('1')
    #响应队列
    def getHtml(self):
        time.sleep(2)
        while True:
            url = self.urlQueue.get()
            #调用封装的函数
            print(url)
            html = self.encphtml(url)
            # self.header = {'User-Agent': self.headers}
            # res = requests.get(url,headers = self.header)
            # html = res.text
            #转化为json 数据
            r = '[{].*[}]'
            htmlover = re.findall(r, html)
            #放到响应队列中
            self.resQueue.put(htmlover[0])
            #清除url队列的任务
            self.urlQueue.task_done()
            print('2')

    #解析网页
    def getContent(self):
        while True:
            print('self.number为', self.number)
            os.mkdir(self.filenames[self.number])
            #从响应队列中依次获取json源码
            html = self.resQueue.get()
            parseJson = json.loads(html)['data']
            print(parseJson)
            #将每个字典遍历
            for oneJson in parseJson:
                print(oneJson)
                try:
                    try :
                        # imgname = oneJson['title']
                        imglist = oneJson['thumbs']
                    except:
                        # imgname = oneJson['mtitle']
                        imglist = oneJson['mthumbs']
                except:
                    continue
                #遍历图片列表
                for imgurl  in imglist:
                    #解析照片名字
                    imgr = imgurl.split('/')
                    imgname = imgr[-1:]
                    imgnameover = imgname[0]
                    imghtml = self.encpbyte(imgurl)
                    keepname = os.path.join(os.getcwd(),self.filenames[self.number],imgnameover)
                    try:
                        with open(keepname,'wb') as f :
                            f.write(imghtml)
                    except:
                        pass
            self.number += 1
            self.resQueue.task_done()

    def run(self):
        #存放所有线程
        thread_list = []
        self.getUrl()
        #创建gethtml的线程
        for i in range(1):
            theadRes = threading.Thread(target=self.getHtml)
            thread_list.append(theadRes)
        #解析的线程
        for i in range(1):
            threadParse = threading.Thread(target=self.getContent)
            thread_list.append(threadParse)
        #所有线程开始run
        for th in thread_list:
            th.setDaemon(True)
            th.start()
        self.urlQueue.join()
        self.resQueue.join()
        print('运行结束')
    #封装一个text网页解析防止冗余
    def  encphtml(self,url):
        self.header = {'User-Agent': self.headers}
        resp = requests.get(url ,headers =self.header)
        html = resp.text
        return html

    # 封装一个字节网页解析防止冗余
    def encpbyte(self,url):
        self.header = {'User-Agent': self.headers}
        resp = requests.get(url, headers=self.header)
        html = resp.content
        return html


if __name__ == '__main__':
    begin = time.time()
    spider = xlSpider()
    spider.run()
    end = time.time()
    print(end-begin)
