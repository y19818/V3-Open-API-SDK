import json
import csv
import hmac
import base64
import datetime
from hashlib import sha256
import requests
import time

#appsecret = "1234".encode('utf-8')  # 秘钥
#data = "xxxxx".encode('utf-8')  # 加密数据
#signature = base64.b64encode(hmac.new(appsecret, data, digestmod=sha256).digest())

# 获取十六进制加密数据
#signature = base64.b64encode(hmac.new(appsecret, data, digestmod=sha256).hexdigest())
timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat().encode("utf8")
apikey = "0bfb03f1-9434-4bdf-81d2-e908dd8e6558"
method = 'GET'.encode("utf8")
requestPath = '/api/v5/market/history-candles'.encode("utf8")
secretkey = b"055009BDFA94CCA5BB7C7D91F08D973E"
total = timestamp+method+requestPath
signature = base64.b64encode(hmac.new(secretkey, total,digestmod=sha256).digest())
print(signature)


IP = ""
备注名 = "lixing"
权限 = "只读"


# 根据每天日期计算当天15:30时ETH价格
def price_day(day):
    #day = '2021-05-05'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36" , "OK-ACCESS-KEY":apikey,"OK-ACCESS-SIGN":signature ,"OK-ACCESS-TIMESTAMP":timestamp ,"OK-ACCESS-PASSPHRASE":"123456"}
    format_time = day+' 15:30:00'
    ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    ts = int(time.mktime(ts))*1000
    ts1 = ts +1
    ts2 = ts -1
    ts1 = str(ts1)
    ts2 = str(ts2)
    response = requests.get("https://www.okex.com/api/v5/market/history-candles?instId=ETH-USDT&bar=30m&after="+ts1+"&before="+ts2, headers = headers)
    result = response.json()["data"][0]
    result[0] = day+' 15:30:00'
    print(result)
    return result


# 根据开始日期、结束日期返回这段时间里所有天的集合
def getDatesByTimes(sDateStr, eDateStr):
    list = []
    datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d')
    list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        list.append(datestart.strftime('%Y-%m-%d'))
    return list

if __name__ == '__main__':
    date_list = getDatesByTimes(sDateStr="2021-05-01",eDateStr="2021-08-27")
    data = []
    for i in date_list:
        
        data.append(price_day(i))

    header = ['开始时间', '开盘价格', '最高价格', '最低价格', '收盘价格', '交易量/张', '交易量/币']
    print(data)

    with open('李星8月.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)