class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        self.major = nums[0]
        count = 1
        
        for x in nums[1:]:
            if count == 0:
                self.major = x
            if x == self.major:
                count = count + 1
            else:
                count = count - 1
        
		#return self.major if nums.count(self.major) > len(nums)//2 else -1
        count = 0
        for x in nums[0:]:
            if x == self.major:
                count = count + 1

        if(count >= len(nums)/2):
            return self.major
        else:
            return -1
