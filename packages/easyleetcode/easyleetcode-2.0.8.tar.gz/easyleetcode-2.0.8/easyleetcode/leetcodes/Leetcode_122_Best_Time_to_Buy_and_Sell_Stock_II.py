class Solution(object):
    def maxProfit(self, prices):
        # sum of prices[i + 1] - prices[i], if prices[i + 1] > prices[i]
        print(zip(prices[0:-1], prices[1:]))
        return sum([y - x for x, y in zip(prices[0:-1], prices[1:]) if x < y])
    
    def maxProfit2(self, prices):
        if prices is None or len(prices) <= 1:
            return 0
        profit = 0
        for i in range(1, len(prices)):
            profit += max(0,prices[i] - prices[i - 1])
        return profit

s=Solution()
print(s.maxProfit([2,1,2,0,1]))
print(s.maxProfit2([2,1,2,0,1]))