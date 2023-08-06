
class Solution:
    def FindContinuousSequence(self, tsum):
        res = []
        i = 1
        j = 2
        curSum = i + j
        while i <= tsum / 2:
            if curSum == tsum:
                res.append(range(i, j + 1))
                j = j + 1
                curSum += j
            elif curSum > tsum:
                curSum -= i
                i += 1
            else:
                j += 1
                curSum += j
        return res
