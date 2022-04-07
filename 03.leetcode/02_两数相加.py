# Definition for singly-linked list.
from typing import List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

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
            befor.next = ListNode(s%10)
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

# 0 -> 1 -> 5 -> 4
l11 = ListNode(9, None)
l12 = ListNode(9, None)
l13 = ListNode(9, None)
l14 = ListNode(9, None)
l11.next = l12
l12.next = l13
l13.next = l14

# 0 -> 9 -> 5 -> 5
l21 = ListNode(9, None)
l22 = ListNode(9, None)
l23 = ListNode(9, None)
l24 = ListNode(9, None)
l25 = ListNode(9, None)
l26 = ListNode(9, None)
l27 = ListNode(9, None)
l21.next = l22
l22.next = l23
l23.next = l24
l24.next = l25
l25.next = l26
l26.next = l27


sol = Solution()
l3 = sol.addTwoNumbers1(l21, l11)
#a = sol.listToInt(l11)
#b = sol.listToInt(l21)
#l3 = sol.intToList(a + b)
while l3 != None:
    print(l3.val)
    l3 = l3.next
