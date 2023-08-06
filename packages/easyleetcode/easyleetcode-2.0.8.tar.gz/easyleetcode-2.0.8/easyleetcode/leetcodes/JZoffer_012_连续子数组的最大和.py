

class Solution:
    def FindGreatestSumOfSubArray(self, array):
        res = max(array)
        temp = 0
        for i in array:
            temp = max(i, temp + i)
            res = max(res, temp)
        return res
