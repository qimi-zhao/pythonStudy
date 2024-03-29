"""
class Solution:
    def isUnique(self, astr: str) -> bool:
        self.array = list(range(1, (ord('z') - ord('A') + 2)))
        
        for i in range(len(astr)):
            num = ord(astr[i]) - ord('A')
            if self.array[num] == 0:
                return False
            else:
                self.array[num] = 0
        
        return True
"""
class Solution:
    def isUnique(self, astr: str) -> bool:
        #如果有大写字母，最多需要58个bit，这里定义64个
        self.bitNum = 0XFFFFFFFFFFFFFFFF

        for i in range(len(astr)):
            loc = ord(astr[i]) - ord('A')
            ret = (self.bitNum & (1 << loc))

            if(ret == 0):
                return False
            else:
                self.bitNum = self.bitNum ^ (1 << loc)
        
        return True
