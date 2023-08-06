
# 使用归并排序的思路求解
class Solution:
    def InversePairs(self, data):
        if len(data) > 1:
            mid = len(data) / 2
            left_half = data[:mid]
            right_half = data[mid:]
            left_count = self.InversePairs(left_half) % 1000000007
            right_count = self.InversePairs(right_half) % 1000000007
            i, j, k, count = len(left_half) - 1, len(right_half) - 1, len(data) - 1, 0
            while i >= 0 and j >= 0:
                if left_half[i] < right_half[j]:
                    data[k] = right_half[j]
                    j = j - 1
                    k = k - 1
                else:
                    data[k] = left_half[i]
                    count += (j + 1)
                    i = i - 1
                    k = k - 1
            while i >= 0:
                data[k] = left_half[i]
                k = k - 1
                i = i - 1
            while j >= 0:
                data[k] = right_half[j]
                k = k - 1
                j = j - 1
            return (count + left_count + right_count) % 1000000007
        else:
            return 0
