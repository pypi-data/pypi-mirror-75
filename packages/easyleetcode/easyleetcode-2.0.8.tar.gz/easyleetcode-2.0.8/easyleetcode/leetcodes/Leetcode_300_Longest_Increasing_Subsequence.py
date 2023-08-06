class Solution:
    def longestIncreasingSubsequence(self, nums):
        if not nums:
            return 0
        
        # f[i]:前i个数字中，以第i个数字结尾的 LIS 长度
        lis = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                # 所有满足条件的 j 中将最大的f[j] 赋予f[i],
                if nums[j] <= nums[i] and lis[i] < 1 + lis[j]:
                    lis[i] = 1 + lis[j]
        return max(lis)
    
    def longestIncreasingSubsequence2(self, nums):
        if not nums:
            return 0
        lis = [1] * len(nums)

        for i in range(1, len(nums)):
            for j in range(i):
                if nums[j] <= nums[i] and lis[i] < 1 + lis[j]:
                    lis[i] = 1 + lis[j]
        print(lis)
        # max value
        max_lis = 0
        # max value index
        index = 0
        for i in range(len(lis)):
            if lis[i] > max_lis:
                max_lis = lis[i]
                index = i
        # Longest_Increasing_Subsequence arr
        result = [0]*max_lis
        for i in range(index,-1,-1):
            if lis[i] == max_lis:
                result[max_lis - 1] = nums[i]
                max_lis-=1

        return result
    
s = Solution()
print(s.longestIncreasingSubsequence([5, 4, 1, 2, 3,1]))
print(s.longestIncreasingSubsequence2([5, 4, 1, 2, 3,1]))


print(s.longestIncreasingSubsequence([4, 2, 4, 5, 3, 7]))
print(s.longestIncreasingSubsequence2([4, 2, 4, 5, 3, 7]))