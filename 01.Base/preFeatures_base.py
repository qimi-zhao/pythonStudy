# -*- coding: utf-8 -*-

from collections import Iterable

"""  高级特性 """

# 切片
"""
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print('L[0:3] = ', L[0:3])
print('L[:3] = ', L[:3])
print('L[1:3] = ', L[1:3])
print('L[-2:] = ', L[-2:])

# test
def trim(input):
    if input == '':
        return input

    str = list(input)
    #print(str)
    while str[0] == ' ':
        str.pop(0)
        if len(str) == 0:
            return ''

    while str[len(str) - 1] == ' ':
        str.pop(-1)
        if len(str) == 0:
            return ''
    
    #print("".join(str))
    return "".join(str)

if trim('hello  ') != 'hello':
    print('测试失败1!')
elif trim('  hello') != 'hello':
    print('测试失败2!')
elif trim('  hello  ') != 'hello':
    print('测试失败3!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败4!')
elif trim('') != '':
    print('测试失败5!')
elif trim('    ') != '':
    print('测试失败6!')
else:
    print('测试成功!')
"""
### 迭代
"""
# 判断对象是否可以迭代
# from collections import Iterable
print(isinstance('abc', Iterable))
print(isinstance([1, 2, 3], Iterable))
print(isinstance(123, Iterable))

# list的迭代
list1 = [1, 2, 3, [4, 5], 'a']
for line in list1:
    print(line)
# list 带下标的迭代 for i, value in enumerate(list)

# dict的迭代
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print('key = ', key, 'value = ', d[key])
# 只迭代value    ：for value in d.values()
# 同时迭代key和值 ：for key, value in d.items()

# test
def findMinAndMax(input):
    if len(input) == 0:
        return (None, None)
    
    min = input[0]
    max = input[0]

    for num in input:
        if num > max:
            max = num
        
        if num < min:
            min = num
    
    return (min, max)

if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
"""

### 列表生成式
"""
list1 = [x * x for x in range(5)]
print(list1)

#  加限制条件
#[x * x for x in range(1, 11) if x % 2 == 2]
#  两层循环的生成
#[m + n for m in 'ABC' for n in 'XYZ']
#  从dict生成list
#[k + '=' + y for k, y in dict.items()]
#  if .. else （if 在for前面必须加else ，相反则不能加else）
#①跟在for后面的if是一个筛选条件，不能带else
#②这是因为for前面的部分是一个表达式，它必须根据x计算出一个结果。

# test
L = ['Hello', 'World', 18, 'Apple', None]
list1 = [ x.lower() if isinstance(x, str) else x for x in L]
print(list1)
"""

### 生成器 generator
# (如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？
# 这样就不必创建完整的list，从而节省大量的空间。)

# ①将列表生成式的[] 换成()
L = [x * x for x in range(10)]
g = (x * x for x in range(10))
#print('获取generator的数据需使用 next(g) = ', next(g))
#for n in g:
#    print(n)

# ②如果一个函数包含 yield 关键字， 则这个函数被称作generator
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'
# 遇yield返回，下次调用next接着执行，直到traceback(StopIteration)

# test
def triangles():
    yield [1]
    yield [1, 1]
    lineNum = 3
    list1 = [1, 1]
    list2 = [] 

    while True:
        for n in range(lineNum):
            if n == 0 or n == lineNum - 1:
                list2.append(1)
            else:
                list2.append(list1[n-1] + list1[n])
            #print(list2)
       
        yield(list2)
        lineNum = lineNum + 1
        list1.clear()
        list1 = list2
        list2 = []

o = triangles()

for i in range(11):
    try:
        x = next(o)
        print(x)
    except StopIteration as e:
        print('Generator return value:', e.value)
        break