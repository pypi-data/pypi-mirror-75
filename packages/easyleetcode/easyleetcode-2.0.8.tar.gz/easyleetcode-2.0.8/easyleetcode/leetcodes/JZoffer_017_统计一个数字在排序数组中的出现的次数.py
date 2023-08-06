
class Solution:
    def GetNumberOfK(self, data, k):
        if len(data) == 0:
            return 0
        i = 0
        j = len(data) - 1
        while i < j and data[i] != data[j]:
            if data[i] < k:
                i += 1
            if data[j] > k:
                j -= 1
        if data[i] != k:
            return 0
        return j - i + 1


class Solution2:
    def GetNumberOfK(self, data, k):
        return data.count(k)
