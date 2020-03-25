import requests
import re
from lxml import etree
import datetime
import pandas as pd
import time
import selenium.webdriver


# Selenium打开视频作者个人网页，并获取页面HTML
driver = selenium.webdriver.Chrome()
driver.get("https://space.bilibili.com/451618887/video?tid=0&keyword=&order=pubdate")
time.sleep(2)
response = driver.page_source
driver.close()


# 分析HTML，获取总页数
html = etree.HTML(response,etree.HTMLParser())
results = html.xpath('//div[@id=\"submit-video-list\"]/ul[@class=\"clearfix cube-list\"]//li/@data-aid')
all_pages = html.xpath("//span[@class=\"be-pager-total\"]/text()")
all_pages = re.findall("\d+",str(all_pages))[0]

# 获取所有页的HTML,获取所有视频链接
video_lastcode_list =[]
for page in range(eval(all_pages)):
    url = "https://space.bilibili.com/451618887/video?tid=0&page={}&keyword=&order=pubdate".format(page+1)
    # 获取该页中HTML
    driver = selenium.webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    response = driver.page_source
    driver.close()
    html = etree.HTML(response, etree.HTMLParser())
    # 获取该页中所有视频链接
    video_lastcode = html.xpath('//div[@id=\"submit-video-list\"]/ul[@class=\"clearfix cube-list\"]//li/@data-aid')
    video_lastcode_list.extend(video_lastcode)

url_list = []  # 所有视频链接的列表
for video_lastcode in video_lastcode_list:
    url = "https://www.bilibili.com/video/" + video_lastcode
    url_list.append(url)
print(url_list)


# 下面开始抓取弹幕
def download(url):  # 定义一个请求函数
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
    request = requests.get(url, headers=headers)
    return request.text,request.content
i = 0
for url in url_list:
    i+=1
    print("正在爬取第{}/{}个视频".format(i,len(url_list)))
    video_url = url
    response = download(video_url)[0]
    oid = re.findall("\d\d/\d\d/(\d{9})/",response)[0]   # 获取该视频oid
    danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid=" + str(oid)  # 拼凑视频弹幕API链接
    response = download(danmu_url)[1]
    html = etree.HTML(response,etree.HTMLParser())
    danmu_list = html.xpath('//d/text()')    # 抓取弹幕内容
    danmu_time_list = [datetime.datetime.fromtimestamp(eval(i.split(",")[4])).strftime("%Y-%m-%d %H:%M:%S") for i in html.xpath("//d/@p")] # 抓取弹幕发表时间
    def judge_class(x):
        x = eval(x)
        if 1<= x <= 3:
            return "滚动弹幕"
        elif x==4:
            return "底端弹幕"
        elif x==5:
            return "顶端弹幕"
        elif x==6:
            return "逆向弹幕"
        elif x== 7:
            return "精准定位弹幕"
        else:
            return "高级弹幕"
    danmu_class_list = [judge_class(i.split(",")[1]) for i in html.xpath("//d/@p")]  # 抓取弹幕类型
    print(danmu_list)
#将抓取到的内容写入csv文件
    print("正在写入……")
    df = pd.DataFrame()
    df["弹幕内容"] = danmu_list
    df["发表时间"] = danmu_time_list
    df["弹幕类型"] = danmu_class_list
    print("一共",len(df),"条弹幕")
    try:
        df.to_csv("take off.csv", mode="a+", header=None, index=None, encoding="gb18030")
        print("第{}个视频的弹幕写入成功".format(i))
    except:
        print("第{}个视频的弹幕写入失败".format(i))
    time.sleep(1)

