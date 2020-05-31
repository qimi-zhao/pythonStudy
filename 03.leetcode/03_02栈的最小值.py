class MinStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.minStack = list()
        self.stack = list()

    def push(self, x: int) -> None:
        self.stack.append(x)
        if not self.minStack or x <= self.minStack[-1]:
            self.minStack.append(x)


    def pop(self) -> None:
        tmp = self.stack.pop()
        if tmp == self.minStack[-1]:
            self.minStack.pop()

    def top(self) -> int:
       return self.stack[-1]


    def getMin(self) -> int:
        if not self.stack:
            return None
        
        return self.minStack[-1]

minStack =  MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)
print(minStack.getMin())
print(minStack.pop())
print(minStack.top())
print(minStack.getMin())