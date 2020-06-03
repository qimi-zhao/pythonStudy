import requests
from bs4 import BeautifulSoup
import logWriter as lw


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

res = requests.get('http://bj.xiaozhu.com/', headers = headers)
print(res)

soup = BeautifulSoup(res.text, 'html.parser')
# 四种解释器
#1 "html.parser"      python内置的标准库，执行速度中，容错能力强              python2.7.3 or 3.2.2 之前的版本中容错能力差
#2 "lxml"             速度快， 容错能力强                                   需要安装C语言库
#3 ["lxml", "xml"] -> "xml"  速度快，唯一支持XML的解析器                     需要安装C语言库
#4 html5lib           最好的容错性，以浏览器的方式解析文档生成HTML5的格式文档  速度慢，不依赖外部扩展库

lf = lw.logWriter()

try:
    lf.write(soup.prettify())
except ConnectionError:
    print('connect Default')

# 解析到的Soup文档可以使用find()和find_all()方法及selector()方法定位需要的元素
# find_all(tag, attibutes, recursive, text, limit, keywords)
# find(tag, attibutes, recursive, text, keywords)

# F12 Element中找到价格标签位置  右键copy -> copy Selector
#page_list > ul > li:nth-child(1) > div.result_btm_con.lodgeunitname > div:nth-child(1) > span > i
price = soup.select('#page_list > ul > li:nth-of-type(1) > div.result_btm_con.lodgeunitname > div:nth-child(1) > span > i')  #定位元素位置并通过selector方法提取
print(price)

# 从一个数据到同类型数据：soup.select()尽量不使用完整selector
# 因为我们复制回来的selector是浏览器上的selector，我们平时在浏览器上看到的都是经过js脚本的加工，所以selector也是经过加工的。
# 而我们程序爬取到的网页并没有经过浏览器加工，所以所需的selector有可能和浏览器上的不一样，也就是为什么我们会得到一个空列表。
# 解决办法 尽量使用较短的selector去定位我们的数据，一般复制回来的selector前半部分可以不要，如果还是没办法准确定位，那再往前加。

#page_list > ul > li > div.result_btm_con.lodgeunitname >  此处截断即可获取到正确数据
prices = soup.select(' div > span > i')
print(prices)
for num in prices:
    print(num)