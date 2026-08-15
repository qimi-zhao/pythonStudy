###################################################
##
##  计算
##  下一次中奖号码
##
##  2022.4.22
##
###################################################

from random import randrange, randint, sample
import xlrd
import numpy as np
import codecs

Loto7_Data_List = []
Loto7_Data_Honsuuji_Cnt = [0 for x in range(0, 38)]
Loto7_Data_Bonus_Cnt = [0 for x in range(0, 38)]

class Loto:
    def __init__(self, kai="", date=[], honsuuji=[], bonus=[]):
        self.kai = kai
        self.date = date
        self.honsuuji = honsuuji
        self.bonus = bonus

def display(balls):
    """
    输出列表中的Loto7号码
    """
    for index, ball in enumerate(balls):
        if index == len(balls) - 2:
            print('|', end=' ')
        print('%02d' % ball, end=' ')
    print()


def random_select(number):
    """
    随机选择一组号码
    """
    red_balls = [x for x in range(1, 38)]
    selected_balls = []  
    selected_balls = sample(red_balls, number) 
    selected_balls.sort()
    selected_balls.append(randint(1, 16))
    return selected_balls    

def getNextNumber(hisData):
    """
    预测下次开奖号码
    """
    while True:
        ret = random_select(5)  # 获取n个随机值  
        ret.append(9)           # 添加生日日期   
        ret.append(3)
        ret.append(25)
        ret.sort()
        li = list(set(ret))     # 去除重复值
        #  去除重复值结果同原list相同 且 该组随机值历史未出现过
        if len(li) == len(ret) and isNotHisData(hisData, li):
            display(ret)        # 打印该组随机值
            return ret

def isNotHisData(hisData, data):
    """
    当前随机值是否历史出现过
    """
    a = np.array(data)
    for dt in hisData:
        b = np.array(dt)
        if (a == b).all():
            return False
    return True

def calcAndDisplay(str, num, data):
    """
    输出各个数字的出现的概率
    """
    honsuujiProbability = {}
    for i in range(1, len(data)):
        honsuujiProbability[i] = data[i]
    sorted_honnsuuji = sorted(honsuujiProbability.items(), key=lambda x : x[1], reverse=True)
    sorted_len = len(sorted_honnsuuji)
    print("概率最大的", num, "个", str,"数字(出现次数)是：")
    for i in range(num):
        print(sorted_honnsuuji[i][0], "(", sorted_honnsuuji[i][1], end="次) | ")
    print()
    print("概率最小的", num, "个", str,"数字(出现次数)是：")
    for i in range(num):
        print(sorted_honnsuuji[sorted_len - i - 1][0], "(", sorted_honnsuuji[sorted_len - i - 1][1], end="次) | ")
    print()


def displayMaxProbabilityNumber():
    global Loto7_Data_Honsuuji_Cnt
    global Loto7_Data_Bonus_Cnt
    """
    输出各个数字的出现的概率
    """
    calcAndDisplay("本番", 7, Loto7_Data_Honsuuji_Cnt)
    calcAndDisplay("补充", 2, Loto7_Data_Bonus_Cnt)

def dissplyNumberProbability():
    global Loto7_Data_List
    global Loto7_Data_Honsuuji_Cnt
    global Loto7_Data_Bonus_Cnt
    """
    输出各个数字的出现的概率
    """
    allCnt = 0
    for i in range(1, len(Loto7_Data_Honsuuji_Cnt)):
        allCnt = allCnt + Loto7_Data_Honsuuji_Cnt[i]

    if allCnt != len(Loto7_Data_List) * 7:
        print("cnt number error")

    outputStr = "各个数字出现的概率: "
    for i in range(1, len(Loto7_Data_Honsuuji_Cnt)):
        outputStr = outputStr + str(i) + ":" + "{:.2f}%".format(Loto7_Data_Honsuuji_Cnt[i]/allCnt) + ","

    print(outputStr)


def print9Number(cnt, data):
    print("最近", cnt, "期未出现过的 9 个数字是：")
    for i in range(1, 38):
        if data[i] == 0:
            print(i, end = " ")
    print() # 换行


def displyNotFoundNum():
    global Loto7_Data_List
    """
    输出最近 N 期未出现的9个数字
    """
    notfoundData = [0 for x in range(38)]
    notFoundDataNum = 37
    cnt = 0
    for item in reversed(Loto7_Data_List):
        cnt += 1
        for i in range(7):
            num = int(item.honsuuji[i])
            if notfoundData[num] == 0:
                notfoundData[num] = 1
                if notFoundDataNum - 1 == 9:
                    print9Number(cnt, notfoundData)
                    return
                else:
                    notFoundDataNum -= 1


def getHistoryData(excelPath):
    global Loto7_Data_List
    global Loto7_Data_Honsuuji_Cnt
    global Loto7_Data_Bonus_Cnt
    """
    读取excel数据
    """
    allData = []
    with codecs.open("data/loto7_data.csv", "r", "utf-8") as outfile:
        allData = outfile.read()

    dataLine = allData.split("\n")
    for i in range(1, len(dataLine)):
        if len(dataLine[i]) == 0:
            break
        data = dataLine[i].split(",")
        kai = str(data[0])
        date = [data[1], data[2], data[3]]
        honsuuji = []
        for j in range(4, 11):
            honsuuji.append(data[j])
            Loto7_Data_Honsuuji_Cnt[int(data[j])] += 1
        bonus = [data[11], data[12]]
        Loto7_Data_Bonus_Cnt[int(data[11])] += 1
        Loto7_Data_Bonus_Cnt[int(data[12])] += 1
        loto = Loto(kai, date, honsuuji, bonus)
        Loto7_Data_List.append(loto)

if __name__ == '__main__':
    """
    主函数
    """
    # loadData.loto7_data()  # 从官网下载所有历史数据
    getHistoryData("data/loto7_data.csv") # 从excel中读取历史数据
    # displyNumberProbability()  # 打印各个数字出现的概率
    displayMaxProbabilityNumber()  # 打印出现次数最多和最少的数字
    displyNotFoundNum()# 打印最近 N 期中未出现的 9 个数字
    
    
    