import requests
import logWriter as lw

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

res = requests.get('http://bj.xiaozhu.com/', headers = headers)
print(res)

#4种连接异常
#1 ConnectionError  : 网络问题（DNS查询失败， 拒绝连接等）
#2 HTTPError        : HTTP返回了不成功的状态码（网页不存在，404等）
#3 Timeout          : 连接超时
#4 TooManyRedirects : 请求超过了最大允许的重定向数

# 所有Requests显示抛出的异常都继承于 requests.exceptions.ResquestException
# 异常后使用try结构可打印此次异常，并继续向下执行

lf = lw.logWriter()

try:
    lf.write(res.text)
except ConnectionError:
    print('connect Default')