class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        bestL = triangle[0][0]
        col = 0

        for l in triangle[1:]:
            if l[col] < l[col+1]:
                bestL = bestL + l[col]
            else:
                bestL = bestL + l[col+1]
                col = col + 1
        
        return bestL
		
		
"""
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        M = len(triangle)
        N = len(triangle[-1])

        dp=[[0]*N for _ in range(M)]
        dp[-1]=triangle[-1]

        for i in range(M - 2, -1, -1):
            for j in range(i,-1,-1):
                dp[i][j] = min(dp[i+1][j+1], dp[i+1][j]) + triangle[i][j]
        return dp[0][0]
"""