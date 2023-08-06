
class Solution:
    def __init__(self):  # 机器人可以倒回来，但不能重复计数。
        self.count = 0

    def movingCount(self, threshold, rows, cols):
        flag = [[1 for i in range(cols)] for j in range(rows)]
        self.findWay(flag, 0, 0, threshold)  # 从（0，0）开始走
        return self.count

    def findWay(self, flag, i, j, k):
        if i >= 0 and j >= 0 and i < len(flag) and j < len(flag[0]) and sum(list(map(int, str(i)))) + sum(
                list(map(int, str(j)))) <= k and flag[i][j] == 1:
            flag[i][j] = 0
            self.count += 1
            self.findWay(flag, i - 1, j, k)
            self.findWay(flag, i + 1, j, k)
            self.findWay(flag, i, j - 1, k)
            self.findWay(flag, i, j + 1, k)
