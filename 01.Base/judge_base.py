# -*- coding: utf-8 -*-

"""  条件判断 """

age = 20
if age >= 20:
    print('your age is ', age)
    print('adult')

age = 6

if age >= 18:
    print('your age is ', age)
    print('adult')
elif age >= 10:
    print('your age is ', age)
    print('teenager')
else:
    print('your age is ', age)
    print('kid')

s = input('your birth day is:')         #input 返回的数据类型是str
birth = int(s)                          #  强制数据类型可用
if birth < 2000:
    print('不是00后')
else:
    print('00后')

# BMI 计算
lenth = float(input('Please input your lenth(cm):')) / 100
height = float(input('Please input your height(kg):'))
bmi = height/(lenth*lenth)
print('your bmi is:', bmi, '%')
if bmi < 18.5:
    print('you\'re too light!')
elif bmi < 25:
    printf('you got a good grade!')
elif bmi < 28:
    print('you are little heave bro!')
else:
    print('seriously, change your self!')