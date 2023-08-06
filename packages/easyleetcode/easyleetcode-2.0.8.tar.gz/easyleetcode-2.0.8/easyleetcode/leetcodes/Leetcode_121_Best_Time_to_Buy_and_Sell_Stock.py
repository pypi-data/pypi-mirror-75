class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        length = len(prices)
        if length == 0:
            return 0
        # low : minmum prices
        max_profit, low = 0, prices[0]
        for i in range(1, length):
            if low > prices[i]:
                low = prices[i]
            else:
                # profit
                temp = prices[i] - low
                if temp > max_profit:
                    max_profit = temp
        return max_profit
    
s=Solution()
print(s.maxProfit([3,2,3,1,2]))
print(s.maxProfit([3,0,3,1,2]))
