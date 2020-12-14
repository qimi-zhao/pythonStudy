# -*- coding: utf-8 -*-
import math

"""  函数 """

# 自动参数检查只能检查出参数数量错误，并不检查参数类型
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-99))

### 空函数
def nop():
    pass        #什么也不做，仅仅让程序运行起来

### 主动参数检查
def my_abs_1(x):
    if not isinstance(x, (int, float)):
        raise TypeError('Bade operand type')
    if x >= 0:
        return x
    else:
        return -x

#print(my_abs_1('A'))

### 多个返回值的函数
""" def move(x, y, step, angle):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny

x, y = move(100, 100, 60, math.pi / 6)
print('x=',x,' y=', y)
l = move(100, 100, 60, math.pi / 6)  # 其实返回值是一个tuple
print('l = ',l) """

# 请定义一个函数quadratic(a, b, c)，接收3个参数，返回一元二次方程 ax^2+bx+c=0 的两个解。
def quadratic(a, b, c):
    anw1= (0 - b + math.sqrt( b * b - 4 * a * c)) / (2 * a)
    anw2= (0 - b - math.sqrt( b * b - 4 * a * c)) / (2 * a)
    return anw1, anw2

# 测试:
print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')

### 默认参数
def power(x, n=2, city='BeiJing'):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s, city

print(power(5))
print(power(5, 2))
print(power(5, city='XiAn'))

### 可变参数
def calc(*numbers):  # 这里会将
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print(calc(1, 2))
print(calc(1, 2, 3))
print(calc(1, 2, 3, 4))

### 关键字参数
def person(name, age, **kw):
    if 'city' in kw:
        # 有city参数
        pass
    if 'job' in kw:
        # 有job参数
        pass
    print('name:', name, 'age:', age, 'other:', kw)

person('Jack', 24, city='Beijing', addr='Chaoyang', zipcode=123456)

""" ### 命名参数
def person(name, age, *, city, job):
    print(name, age, city, job)

# 和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数
# 命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错

# 如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符
def person(name, age, *args, city, job):
    print(name, age, args, city, job)

#命名关键字参数可以有缺省值，从而简化调用
def person(name, age, *, city='Beijing', job):
    print(name, age, city, job) """

### 参数组合
# 在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数.
# 这5种参数都可以组合使用。但是请注意，参数定义的顺序必须是：
# 必选参数、默认参数、可变参数、命名关键字参数和关键字参数
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)


### 测试
def product(*numbers):
    if len(numbers):
        pass
    else:
        raise TypeError('Bade operand type')
    sum = 1
    for i in numbers:
        sum = sum * i
    return sum

print('product(5) =', product(5))
print('product(5, 6) =', product(5, 6))
print('product(5, 6, 7) =', product(5, 6, 7))
print('product(5, 6, 7, 9) =', product(5, 6, 7, 9))
if product(5) != 5:
    print('测试失败!')
elif product(5, 6) != 30:
    print('测试失败!')
elif product(5, 6, 7) != 210:
    print('测试失败!')
elif product(5, 6, 7, 9) != 1890:
    print('测试失败!')
else:
    try:
        product()
        print('测试失败!')
    except TypeError:
        print('测试成功!')

### 递归函数
def fact(n):
    if n == 1:
        return 1
    return n * fact(n-1)

print(fact(5))

# 尾递归是指在函数返回的时候，调用自身本身，并且，return语句不能包含表达式。
# 这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况
""" def fact(n):
    return fact_iter(n, 1) """

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)

### test 汉诺塔问题
def move(n, a, b, c):
    if n == 1:
        print('move', a, '-->', c)
    else:
        move(n-1, a, c, b)
        move(1, a, b, c)
        move(n-1, b, a, c)

move(6, 'A', 'B', 'C')