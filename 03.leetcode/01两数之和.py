#给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。
#你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。
#你可以按任意顺序返回答案。

#输入：nums = [2,7,11,15], target = 9
#输出：[0,1]
#解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。

from typing import List

class Solution:
    def twoSum(self, nums:List[int], target:int) -> List[int]:
        if len(nums) < 2:
            return []
        nums = sorted(nums)
        # return self.findIndex(target, 0, len(nums) - 1, nums)
        return self.findIndexByDict(nums, target)

    def findIndex(self, target : int, start, end, nums: List[int]) -> List[int]:

        if start >= end:
            return []
        elif nums[start] + nums[end] == target:
            return [start, end]
        elif nums[start] + nums[end] > target:
            return self.findIndex(target, start, end - 1, nums)
        else:
            return self.findIndex(target, start + 1, end, nums)

    def findIndexByDict(self, nums:List[int], target:int) -> List[int]:
        hashmap = {}
        for index, num in enumerate(nums):
            another_num = target - num
            if another_num in hashmap:
                return [hashmap[another_num], index]
            hashmap[num] = index
        return None
        

sol = Solution()
print(sol.twoSum([1], 10))
print(sol.twoSum([1, 2, 3, 4, 5, 6], 10))
