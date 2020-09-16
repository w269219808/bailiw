import requests
import re
import csv
import json
import datetime

foodsId = '商品'
def getJson():

    name = input('请输入取消的商品id:')
    global foodsId
    foodsId = str(name)


    posturl = 'https://sycm.taobao.com/flow/v3/monitor/item/delete.json?token=4bdb5ea91'

    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    head = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Length': '98',
    'Origin': 'https://sycm.taobao.com',
    'Referer': 'https://sycm.taobao.com/mc/ci/config/rival?activeKey=item',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }

    path = 'D:/Python/sycm/mycookies.txt'   #把cookies保存到文本文件中，用cookies登陆美滋滋
    with open(path,'r')as f:
        mycookies = f.read()
    mycookies = mycookies.split(';')
    cookies = {}
    for cookie in mycookies:
        name,value = cookie.strip().split('=',1)
        cookies[name] = value

    html = ''



    idData = {'itemId':foodsId,'_':'1594798795623'}


    r = requests.post(posturl, data=idData, cookies=cookies,headers=head,verify=False)

    r.encoding = r.apparent_encoding
    html += r.text
    return html


if __name__ == "__main__":

    jsontxt = getJson()

    print(jsontxt)


