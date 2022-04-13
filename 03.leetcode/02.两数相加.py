# Definition for singly-linked list.
import sys, os
from json import tool
from typing import List

# 导入相对路径工程类
this_dir = os.path.dirname(__file__) + '/../lib' #工程类路径
sys.path.append(this_dir) # 添加进系统资源列表
from tool import ListNode
from tool import makeData

class Solution:
    def addTwoNumbers1(self, l1: ListNode, l2: ListNode) -> ListNode:
        l3 = ListNode(0, None)
        befor = l3
        flag = 0
        while( l1 or l2):
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            s = flag + x + y
            flag = s // 10
            befor.next = ListNode(s % 10)
            befor = befor.next
            if(l1 != None): l1 = l1.next 
            if(l2 != None): l2 = l2.next 
        
        if flag == 1:
            befor.next = ListNode(1, None)
        return l3.next

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        l3 = ListNode(0, None)
        befor = l3
        flag = 0
        while l1 != None or l2 != None:
           if l1 == None:
               if l2.val + flag < 10:
                   after = ListNode(l2.val + flag, None)
                   flag = 0
               else:
                   after = ListNode(l2.val + flag - 10, None)
                   flag = 1
               l2 = l2.next
           elif l2 == None:
               if l1.val + flag < 10:
                   after = ListNode(l1.val + flag, None)
                   flag = 0
               else:
                   after = ListNode(l1.val + flag - 10, None)
                   flag = 1
               l1 = l1.next
           else:
               if l2.val + l1.val + flag < 10:
                   after = ListNode(l2.val + l1.val + flag, None)
                   flag = 0
               else:
                   after = ListNode(l2.val + l1.val - 10 + flag, None)
                   flag = 1
               l2 = l2.next
               l1 = l1.next
                   
           befor.next = after
           befor = after

        if flag == 1:
            after = ListNode(1, None)
            befor.next = after
        return l3.next
    
    def listToInt(self, l1: ListNode) -> int:
        i = 0
        val = 1
        while l1 != None:
           i = i + l1.val * val 
           l1 = l1.next
           val = val * 10
        return i

    def intToList(self, val) -> ListNode:
        l1 = ListNode(0, None)
        bf = l1
        while val >= 10:
            af = ListNode(val % 10, None)
            bf.next = af
            bf = af
            val = int(val / 10)
        af = ListNode(val, None)
        bf.next = af
        return l1.next

sol = Solution()
mk = makeData()

# 0154 + 0955
l1 = mk.createList([0, 1, 5, 4])
l2 = mk.createList([0, 9, 5, 5])
l3 = sol.addTwoNumbers1(l1, l2)

output = 0
coefficient = 1
while l3 != None:
    output = output + l3.val * coefficient
    coefficient = coefficient * 10
    l3 = l3.next
print(output)

# 9999 + 9999999
l1 = mk.createList([9, 9, 9, 9])
l2 = mk.createList([9, 9, 9, 9, 9, 9, 9])
l3 = sol.addTwoNumbers1(l1, l2)
output = 0
coefficient = 1
while l3 != None:
    output = output + l3.val * coefficient
    coefficient = coefficient * 10
    l3 = l3.next
print(output)