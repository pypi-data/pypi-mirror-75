class Solution(object):
    def maxProfit(self,prices,k=2):
        if not prices: return 0
        if k >= len(prices): return self.solveMaxProfit(prices)
        
        # [i] : at most i transactions.
        g =[0]*(k+1) # global profit
        l =[0]*(k+1) # local profit
        for i in range(len(prices)-1):
            # transactions profit
            diff = prices[i + 1] - prices[i]
            for j in range(k,0,-1):
                 # i次局部最大收益，是j-1次全局最大收益+diff 或者 j-1次局部最大收益+diff，取最大的
                l[j] = max(g[j - 1] + max(diff, 0), l[j] + diff)
                g[j] = max(l[j], g[j])
        return g[k]
    
    def solveMaxProfit(self,prices):
        res = 0
        for i in range(1,len(prices)):
            res += max(0,prices[i] - prices[i - 1])
        return res
    

s=Solution()
print(s.maxProfit([4,4,6,1,1,4,2,5],k=2))
print(s.maxProfit([4,4,6,1,1,4,2,5],k=8))

