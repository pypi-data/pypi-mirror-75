
class Solution:
    def LastRemaining_Solution(self, n, m):
        if not n and not m:
            return -1
        res = range(n)
        i = 0
        while len(res) > 1:
            i = (m + i - 1) % len(res)
            res.pop(i)
        return res[0]


class Solution2:
    def LastRemaining_Solution(self, n, m):
        if n == 0:
            return -1
        s = 0
        for i in range(2, n + 1):
            s = (s + m) % i
        return s
