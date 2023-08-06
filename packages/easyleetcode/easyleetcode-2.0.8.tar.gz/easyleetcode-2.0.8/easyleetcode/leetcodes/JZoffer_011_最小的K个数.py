
class Solution:
    def GetLeastNumbers_Solution(self, tinput, k):
        tinput.sort()
        result = []
        if k > len(tinput): return []
        for i in range(k):
            result.append(tinput[i])
        return result
