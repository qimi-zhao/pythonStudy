import os
from typing import List

# 最简单的list元子
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 创建数据类
class makeData:
    # 根据数组创建链表
    def createList(self, data: List) -> ListNode:
        output = ListNode(0, None)
        befor = output
        for num in data:
            after = ListNode(num, None)
            befor.next = after
            befor = after
        return output.next
