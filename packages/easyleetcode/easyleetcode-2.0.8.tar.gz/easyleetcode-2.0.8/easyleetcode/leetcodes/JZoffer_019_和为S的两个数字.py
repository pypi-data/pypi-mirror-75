
class Solution:
    def FindNumbersWithSum(self, array, tsum):
        if len(array)<2:
            return []
        i = 0
        j = len(array)-1
        while i < j:
            if array[i]+array[j] > tsum:
                j -= 1
            elif array[i]+array[j] < tsum:
                i += 1
            else:
                return [array[i],array[j]]
        return []