class Solution:
    
    def jump(self, nums):
        res = 0
        n = len(nums)
        #  cur 当前能到达的最远位置，last 上一步(res+=1)能到达的最远位置
        last = 0
        cur = 0
        for i in range(n-1):
            cur = max(cur, i + nums[i])
            if i == last:
                last = cur
                res+=1
                if cur >= n - 1: break
        return res

    
solution = Solution()
print(solution.jump([2,3,1,1,4]))