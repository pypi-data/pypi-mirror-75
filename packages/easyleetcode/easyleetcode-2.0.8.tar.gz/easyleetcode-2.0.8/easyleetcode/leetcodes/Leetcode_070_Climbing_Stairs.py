class Solution(object):
    def climbStairs(self, n):
        if n <= 1:
            return 1
        # Stairs 1 = 1 , Stairs 2 = 1+1 = 2
        dp = [1] * 2
        for i in range(2, n + 1):
            # Stairs 3 = Stairs 2 + Stairs 1
            # Stairs 4 = Stairs 3 + Stairs 2
            dp[1], dp[0] = dp[1] + dp[0], dp[1]
        return dp[1]
