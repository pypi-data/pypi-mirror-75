
class Solution:
    def __init__(self):
        self.sum = 0

    def Sum_Solution(self, n):
        if n <= 0:
            return 0
        self.getSum(n)
        return self.sum

    def getSum(self, n):
        self.sum += n
        n = n - 1
        return n > 0 and self.getSum(n)


class Solution2:
    def Sum_Solution(self, n):
        return n and self.Sum_Solution(n - 1) + n
