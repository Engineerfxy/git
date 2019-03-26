import requests
import time
from lxml import etree
#这个库需要安装一个插件 PhantomJS 百度一下 就好了
from selenium import webdriver
import json


# 股票代码名://tr/td[2]
# 股票名://tr/td[3]
# 获取网页的Url 传入股票代码和股票名
def get_page(stock_code,stock_name,f):
    #每次取多少页交易细节
    for page in range(1,20):
        json_ulr = "https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SH{}&hl=0&source=trans&page={}&q=%20".format(stock_code,page)
        # print(json_ulr)
        get_msg(json_ulr,stock_code,stock_name,f)
# 获取网页的信息  传入url ,股票代码和股票名
def get_msg(url,stock_code,stock_name,f):
    html = requests.get(url, headers=headers)
    try :
        res_dict = json.loads(html.text)
        for res_one in res_dict["list"]:
        #用户id
            user_id = res_one['user_id']
        #用户名称
            screen_name = res_one['user']['screen_name']
        #日期
            timeBefore = res_one['timeBefore']
        #类型
            text = res_one['text']
        #股票代码
            stockcode = stock_code
        # 股票名
            stockname = stock_name
        #信息来源
            source = res_one['source']
        #写入txt中
            # print(str(user_id)+','+str(screen_name)+','+str(timeBefore)+','+str(text)+','+str(stockcode)+','+str(stockname)+','+str(source))
            f.write(str(user_id)+','+str(screen_name)+','+str(timeBefore)+','+str(text)+','+str(stockcode)+','+str(stockname)+','+str(source))
            f.write('\n')
    except:
        print("这页有错")
        pass
#从沪深300获取股票代码
def get_stock():
    # lushenurl = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHSZZS&sty=SHSZZS&st=0&sr=-1&p=1&ps=50&js=var%20gnKkFdLY={pages:(pc),data:[(x)]}&code=000300&rt=51294587%20HTTP/1.1"
    lushenheaders = {
        "Cookie":"qgqp_b_id=5277d9c523b1210c476a73c66f871343; st_pvi=80844961049130; st_sp=2018-10-03%2016%3A23%3A39; EMSTtokenId=f9a151846da88a5708a3c52cbdc8941b; HAList=a-sz-300015-%u7231%u5C14%u773C%u79D1; em_hq_fls=js; st_si=07941052369454; st_asi=delete; st_sn=5; st_psi=20181006210543908-0-8395675191",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    # response = requests.get(url=lushenurl,headers = lushenheaders)
    # response.encoding = "utf-8"
    # print(response.text)

    diver = webdriver.PhantomJS()
    diver.get("http://data.eastmoney.com/other/index/hs300.html")
    #写入txt文件中
    f = open('gupiaoover.txt','a',encoding="utf-8")
    #循环6页
    #    for count in range(1,7): 这是正常的操作的循环
    #但是可能会你电脑不好 可能需要1个小时左右才能跑完 所以会导致与服务器失去 连接
    #你有两种办法 一种是: 减少交易页数 或者 减少 一次循环的页数
    # 看你自己的电脑了  我电脑一开跑了2页 就 断链了一次 所以有大概100条左右的重复数据 ,因为数据较少我就没去重了,
    for count in range(1,7):
        print(count)
        diver.find_element_by_id("PageContgopage").clear()
        diver.find_element_by_id("PageContgopage").send_keys(count)
        diver.find_element_by_class_name("btn_link").click()
        time.sleep(3)
        # diver.save_screenshot("ok.png")
        # input()
        html = diver.page_source
        paraseobj = etree.HTML(html)
        #股票代码
        stock_code_list = paraseobj.xpath('//tbody/tr/td[2]/a')
        # 股票名字
        stock_name_list = paraseobj.xpath('//tbody/tr/td[3]/a')
        for each_code,each_name in zip(stock_code_list,stock_name_list):
            print(each_code.text,each_name.text)
            get_page(each_code.text,each_name.text,f)
        time.sleep(1)
        # diver.save_screenshot("{}page.png".format(count))
    f.close()





if __name__ == '__main__':
    headers = {
        #这个雪球网的cookie 要用你自己的cookie 不然可能不一定可以...
        'Cookie': '_ga=GA1.2.659966899.1538549716; device_id=15fb0949a564b39311e28bd39018b0e0; s=ee12c9lp7t; __utmz=1.1538550750.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); bid=8c70a97bf662fad0d3ee594606c9b664_jmsu25z6; aliyungf_tc=AQAAADpmtD2TbQ4At7ZmcrelbcXTBXx+; Hm_lvt_1db88642e346389874251b5a1eded6e3=1538549717,1538830831; __utma=1.659966899.1538549716.1538555499.1538830831.3; __utmc=1; _gid=GA1.2.1507505515.1538830859; xq_a_token.sig=5SWm2kWrzAOTikx7CWCYDxJo-3o; xq_r_token.sig=OeiO8iiNsHe_ULfkOZX6eIdXtZI; __utmb=1.15.8.1538833011592; xq_a_token=55cb38b6421f991010bf22add0d6300ac5521da7; xqat=55cb38b6421f991010bf22add0d6300ac5521da7; xq_r_token=69360d26098f90e8cc27061bcae91acb329c3344; xq_token_expire=Wed%20Oct%2031%202018%2022%3A07%3A31%20GMT%2B0800%20(CST); xq_is_login=1; u=1938802208; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1538834858; _gat_gtag_UA_16079156_4=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
# html = requests.get(xueqiuurl,headers=headers)
# res_dict = json.loads(html.text)
# for i in res_dict["list"]:
#     print(i)
    get_stock()

