# -*- coding: utf-8 -*-

### 输出 printf
print('Hi, %s, you have $%d' % ('Michael', 10000))
print('%2d-%02d' % (3, 1))
print('%.2f' % 3.1415926)
print('Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125))


"""  基本数据 """
### 编码格式
print(ord('A'))
print(ord('中'))
print(chr(25991))

### byte类型的数据
x = b'ABC'
print(x)
y = b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
print(y)
print('中文'.encode('gb2312'))

### 字符串 <-> list
str1 = "12345"
list1 = list(str1)
str2 = "123 sjhid dhi"
list2 = str2.split() #or list2 = str2.split(" ")
str3 = "www.google.com"
list3 = str3.split(".")

str4 = "".join(list3)
str5 = ".".join(list3)
str6 = " ".join(list3)


### List (同类型)
classmates = ['Michael', 'Bob', 'Tracy']
classmates.sort()
print(len(classmates))
print(classmates)
# index
print(classmates[0])
print(classmates[-1])
# add
classmates.append('Adam')
print(classmates[0])
print(classmates[-1])
# del(pop 函数，无参时丢弃最后一个)
classmates.pop(2)
print(classmates)
# change
classmates[1] = 'Sarah'
print(classmates)

# 不同类型数据
L = ['Apple', 123, True]
S = ['python', 'java', ['asp', 'php'], 'scheme']

### tuple  元组 ，和list非常类似，但是tuple一旦初始化就不能修改
### （此处不能修改指的是指向不能修改（如果元祖元素有list，则此list不可变，list元素可变））
classmates = ('Michael', 'Bob', 'Tracy')

### 字典值
### 查找和插入的速度极快，不会随着key的增加而变慢；
### 需要占用大量的内存，内存浪费多(用空间换时间)
dic = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
# 判断key是否存在
print('Bob' in dic)
print(dic.get('Bob1'))
#echo
print(dic['Bob'])
# add
dic['Zhao'] = 100
print(dic['Zhao'])
# delete
dic.pop('Bob')


### set和dict类似，也是一组key的集合，但不存储value。
### 由于key不能重复，所以，在set中，没有重复的key。
s = set([1, 2, 3])
print(s)