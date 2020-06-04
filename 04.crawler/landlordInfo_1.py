###################################################
##
##  爬取
##  标题，地址，价格，房东名字，房东性别，房东头像
##
##  2020.6.4
##
###################################################


from bs4 import BeautifulSoup
import requests
import time
import logWriter as lw


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

lf = lw.logWriter()

#判断性别的函数
def judgment_sex(class_name):
    if class_name == ['member_ico1']:
        return '女'
    else:
        return '男'

#获取详细页URL的函数
def get_links(url):
    wb_data = requests.get(url, headers = headers)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    links = soup.select('#page_list > ul > li > a')

    for link in links:
        href = link.get("href")
        #lf.write(str(href))
        get_info(href)

#获取网页信息的函数
def get_info(url):
    wb_data = requests.get(url, headers = headers)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    #lf.write(soup.prettify())

    tittles = soup.select('div.pho_info > h4')              #标题
    addresses = soup.select('span.pr5')                     #地址
    prices = soup.select('div.day_l > span')   #价格
    imgs = soup.select('div.js_box.clearfix > div.member_pic > a > img')   #图
    names = soup.select('div.js_box.clearfix > div.w_240 > h6 > a')        #名字
    sexs = soup.select('div.js_box.clearfix > div.member_pic > div')       #性别
    #print(tittles)
    #print(addresses)
    #print(prices)
    #print(imgs)
    #print(names)
    #print(sexs)

    for tittle, address, price, img, name, sex in zip(tittles, addresses, prices, imgs, names, sexs):
        data = {
            'tittle':tittle.get_text().strip(),
            'address':address.get_text().strip(),
            'price':price.get_text(),
            'img':img.get("src"),
            'name':name.get_text(),
            'sex':judgment_sex(sex.get("class"))
        }
        
        #print(str(data))
        lf.write(str(data))
    

if __name__ == '__main__':
    lf.clean()

    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1,3)]
    lf.write("       ".join(urls))

    for single_url in urls:
        get_links(single_url)
        time.sleep(2)

