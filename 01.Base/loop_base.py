# -*- coding: utf-8 -*-

"""  循环 """

### for in 循环
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print('name is',name)

sum = 0
for x in range(100):
    sum = sum + x
print('for loop, 1..100 sum is ', sum)

### while 循环
count = 100
sum = 0
while count > 0:
    sum = sum + count
    count = count - 2
print('while loop 1..100,delim 2, sum is ', sum)

### break or counitue also useable.