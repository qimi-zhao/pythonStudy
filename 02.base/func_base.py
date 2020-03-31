# -*- coding: utf-8 -*-

from collections import Iterable
import math
from operator import itemgetter

### 函数式编程

###  Functional Programming，虽然也可以归结到面向过程的程序设计，但其思想更接近数学计算。
# 函数式编程的一个特点就是，允许把函数本身作为参数传入另一个函数，还允许返回一个函数！

###  高阶函数（函数名也是变量，可以赋值和被赋值,可以作为函数参数）
def add(x, y, f):
    return f(x) + f(y)

print(add(-5, 6, abs))


### map 和 reduce
# map()函数接收两个参数，一个是函数，一个是Iterable，
# map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
def f(x):
    return x * x

#返回值是Iterator 不能直接print
print(list(map(f, [1, 2, 3, 4, 5, 6, 7])))

# 再看reduce的用法。reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，
# 这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
def add(x, y):
    return x + y

# python3 以后functools模块好像不能pip安装了？
#print(reduce(add, [1, 2, 3, 4, 5]))

#test
def normalize(str):
    # capitalize() 字符串第一个首字母大写
    # title() 字符串内所有单词首字母大写
    #return str.capitalize()
    str = str.lower()
    ch = str[0]
    ch = chr(ord(ch) - ord('a') + ord('A'))
    str = ch + str[1:]
    return str

L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)


### filter()函数 : 过滤序列

# 过滤掉一个序列中的偶数，只留下奇数
def is_odd(n):
    return n % 2 == 1

print(list(filter(is_odd, [1, 2, 3, 4, 5, 6])))

# 用filter求素数
def _odd_iter(): # 构造一个从3开始的奇数序列
    n = 1
    while True:
        n = n + 2
        yield n

def _not_divisible(n): # 筛选函数
    return lambda x: x % n > 0

def primes():   # 生成器
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列第一个数
        yield n
        # 筛选掉能被2，3，5，7。。整除的数
        it = filter(_not_divisible(n), it) # 构造新序列

# 打印1000以内的素数：
for n in primes():
    if n < 10:
        print(n)
    else:
        break

# test  回文数
def is_palindrome(x):
    x = str(x)
    return x == x[::-1]

output = filter(is_palindrome, range(1, 100))
print('1~1000:', list(output))
if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
    print('测试成功!')
else:
    print('测试失败!')


###   sorted 排序算法

# 直接对list排序
print(sorted([36, 5, -12, 9, -21]))   # 默认排序
print(sorted([36, 5, -12, 9, -21], key=abs))   # 条件默认排序

print(sorted(['bob', 'about', 'Zoo', 'Credit']))   # 默认排序
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True))  # 条件反向排序

#test
students = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

print(sorted(students, key=itemgetter(0)))
print(sorted(students, key=lambda t: t[1]))
print(sorted(students, key=itemgetter(1), reverse=True))


### 返回函数 ： 函数作为返回值