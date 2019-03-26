import csv
import re

f = open("gupiaoover.txt","r",encoding="utf-8")
# f2 = open("shares1.csv",'a',encoding='utf-8',newline="")
f3 = open("shareslexcel1.txt",'w',encoding="utf-8")
f3.write("用户id,用户名,日期,类型,股票代码,股票名,价格,信息来源")
f3.write("\n")
# write = csv.writer(f2)
# write.writerow(["用户id",'用户名','日期','类型(买入,卖出,关注)','股票代码','股票名','价格','信息来源'])
for each_text in f:
    try:
        test= each_text.split(',')
        if  "买入" in test[3]:
            price = re.findall(r'以([\s\S]*?)买入',test[3])
            # write.writerow([test[0], test[1], test[2],'买入',"SH:"+test[4],test[5],price[0],test[6]])
            f3.write(test[0]+','+test[1]+','+test[2]+','+'买入'+','+test[4]+','+test[5]+','+price[0]+','+test[6])
        if "卖出" in test[3]:
            price = re.findall(r'以([\s\S]*?)卖出', test[3])
            # write.writerow([test[0], test[1], test[2], '卖出', "SH:"+test[4], test[5], price[0], test[6]])
            f3.write(test[0]+','+test[1]+','+test[2]+','+'卖出'+','+test[4]+','+test[5]+','+price[0]+','+test[6])
        if "关注" in test[3]:
            price1 = re.findall(r'在([\s\S]*?)时关注股票', test[3])
            price2 = re.findall(r"当前价([\s\S]*?)。",test[3])
            if price1:
                # write.writerow([test[0], test[1], test[2], '关注', "SH:"+test[4], test[5], price[0], test[6]])
                f3.write(test[0]+','+test[1]+','+test[2]+','+'关注'+','+test[4]+','+test[5]+','+price1[0]+','+test[6])
            if price2:
                f3.write(test[0]+','+test[1]+','+test[2]+','+'关注'+','+test[4]+','+test[5]+','+price2[0]+','+test[6])

    except:
        #难免会有数据出现不对称的效果
        #100条大概有15条左右的问题数据,不在你的类型之中 我就忽略了
        print("出现了错误")
        pass
f.close()
# f2.close()
f3.close()


