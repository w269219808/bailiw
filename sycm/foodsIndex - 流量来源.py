import requests
import re
import csv
import json
import datetime
 
foodsId = '商品'
 
def getJson():

    name = input('请输入爬取的商品id:')
    global foodsId
    foodsId = str(name)

    t = datetime.date.today() - datetime.timedelta(days=1)  #获取最近30天的数据
   # date = '2020-06-22'  #定义找查的截至时间
    start_url = 'https://sycm.taobao.com/flow/v3/monitor/item/trend.json?dateType=day&dateRange={}%7C{}&cateId=0&itemId={}&device=0&sellerType=-1'.format(t,t,name)

    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
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
    r = requests.get(start_url,headers=header,cookies=cookies,timeout=60)
    r.encoding = r.apparent_encoding
    html += r.text
    return html
 
def trans(html):
    datas = json.loads(html)
    if datas['code'] == 5810:
        return ''

    url = 'http://www.amingtool.com/getdata.php'
    head = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '23',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'Hm_lvt_9e811481d4b93d78ef0e62012807f1f7=1589437448,1589505884,1589592774,1589946853; Hm_lpvt_9e811481d4b93d78ef0e62012807f1f7=1589946853; Hm_lvt_459734649f53a7fd3b34ae4709c35060=1589437448,1589505884,1589592774,1589946853; Hm_lpvt_459734649f53a7fd3b34ae4709c35060=1589946853',
    'Host': 'www.amingtool.com',
    'Origin': 'http://www.amingtool.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.amingtool.com/trans',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    payRateIndex = {'type': 'zfzhlzs', 'val[]': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
    uvIndex = {'type': 'llzs', 'val[]': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
    tradeIndex = {'type': 'jyzs', 'val[]': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
    payByrCntIndex = {'type': 'kqzs', 'val[]': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}


    for i in range(len(datas['data']['payRateIndex'])):
        payRateIndex['val[]'][i] = datas['data']['payRateIndex'][i]
        uvIndex['val[]'][i] = datas['data']['uvIndex'][i]
        tradeIndex['val[]'][i] = datas['data']['tradeIndex'][i]
        payByrCntIndex['val[]'][i] = datas['data']['payByrCntIndex'][i]



    payRate = requests.post(url, data=payRateIndex, headers=head,verify=False)
    uv = requests.post(url, data=uvIndex, headers=head,verify=False)
    trade = requests.post(url, data=tradeIndex, headers=head,verify=False)
    payByrCnt = requests.post(url, data=payByrCntIndex, headers=head,verify=False)

    payRate = json.loads(payRate.text)   #将返回的json转换成字典， 然后读取就可以了
    uv = json.loads(uv.text) 
    trade = json.loads(trade.text) 
    payByrCnt = json.loads(payByrCnt.text) 

    t = datetime.date.today() - datetime.timedelta(days=31)
    index = []
    for i in range(len(payRate['data'])):

        t = t + datetime.timedelta(days=1)

        if(payByrCnt['data'][i]==0):
            kedanjia = 0
        else:
            kedanjia = trade['data'][i] / payByrCnt['data'][i]

        uvPrice = trade['data'][i] / uv['data'][i]
        index.append([t,payRate['data'][i],uv['data'][i],trade['data'][i],payByrCnt['data'][i],kedanjia,uvPrice])
        
    return index


 
def download(data):
    if data =="":
        print("大概率cookies过期")
        return
    print('='*20,'正在保存商品信息','='*20,'\n')
    path = 'D:/Python/sycm/{}.csv'.format(foodsId)
    try:
        f = open(path,"w",newline="",encoding='utf-8-sig')
        writer = csv.writer(f)
        writer.writerow(['日期','支付转化率','访客数','交易金额','付款人数','客单价','uv价值'])
        writer.writerows(data)
        print('='*20,'保存成功','='*20,'\n')
    except:
        print('保存失败')
    f.close()
 
 
def main():
    while True:
        html = getJson()
        taobaoindex = trans(html)
        download(taobaoindex)


 
if __name__ == "__main__":
    main()