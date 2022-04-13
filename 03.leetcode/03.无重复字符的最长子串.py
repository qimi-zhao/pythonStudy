
###########################################################
#
# 给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串 的长度。
#
###########################################################
class Solution:
    ###########################################################
    #
    # 计算最长子串函数
    #
    ###########################################################
    def lengthOfLongestSubstring1(self, s: str) -> int:
        if len(s) <= 1:                                       # 长度小于1时返回长度
            return len(s)

        max = 0                                               # 最大长度
        while len(s) > max:                                   # 剩下字符串大于最大长度才会寻找
            length, start = self.lengthOfLongeFromStart(s)    # 计算从当前位置开始最长不重复子串长度
            max = max if max > length else length             # 记录最大值
            s = s[start:]                                     # 更新起始位置
        
        return max

    ###########################################################
    #
    # 计算从开头开始不重复字符长度
    #
    ###########################################################
    def lengthOfLongeFromStart(self, s: str) -> int:
        dict = { "start": 0}                                  # 用来存放字母上一次位置的字典数据
        index = 1                                             # 字符下标，从1开始（方便计算）
        for char in s:
            if char in dict:                                  # 字符出现过，则返回长度
                return index - 1, dict.get(char)              # 返回最大长度，和下一次的开始位置
            else:
                dict[char] = index
            index = index + 1
        return len(s), len(s)                                 # 从未重复字符，则返回总长度


    ###########################################################
    #
    # 优秀的总是别人！
    #
    ###########################################################
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        dict = {}
        start, ans = 0, 0
        for index in range(len(s)):
            if s[index] in dict:
                start = max(dict[s[index]], start)
            ans = max(ans, index - start + 1)
            dict[s[index]] = index + 1
        return ans;


sol = Solution()
print(sol.lengthOfLongestSubstring("dvdf"))
print(sol.lengthOfLongestSubstring("bbb"))
print(sol.lengthOfLongestSubstring("pwwkew"))
print(sol.lengthOfLongestSubstring("au"))
print(sol.lengthOfLongestSubstring("abba"))
print(sol.lengthOfLongestSubstring("nfpdmpi"))
print(sol.lengthOfLongestSubstring("abcabcbb"))
print(sol.lengthOfLongestSubstring("tmmzuxt"))