#coding:utf-8


def ahead_one():
    a = [i for i in range(1,11)]
    b = a.pop(2)              ###  此处pop的参数是成员下标  并不是成员的值
    a.append(b)
    return a

if __name__ =="__main__":
    print(ahead_one())