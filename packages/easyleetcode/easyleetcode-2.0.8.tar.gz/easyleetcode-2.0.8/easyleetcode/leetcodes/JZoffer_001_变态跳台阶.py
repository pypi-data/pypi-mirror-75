'''

一只青蛙一次可以跳上1级台阶，也可以跳上2级……它也可以跳上n级。求该青蛙跳上一个n级的台阶总共有多少种跳法。

思路：n=0时,f(n)=0；n=1时,f(n)=1；n=2时,f(n)=2；假设到了n级台阶，我们可以n-1级一步跳上来，也可以不经过n-1级跳上来，所以f(n)=2*f(n-1)。

推公式也能得出：

n = n时：f(n) = f(n-1)+f(n-2)+...+f(n-(n-1)) + f(n-n) = f(0) + f(1) + f(2) + ... + f(n-1)

由于f(n-1) = f(0)+f(1)+f(2)+ ... + f((n-1)-1) = f(0) + f(1) + f(2) + f(3) + ... + f(n-2)

所以f(n) = f(n-1)+f(n-1)=2*f(n-1)
'''


class Solution:
    def jumpFloorII(self, number):
        if number <= 0:  return 0
        if number == 1: return 1
        if number == 2: return 2
        result = [1, 2]
        for i in range(2, number):
            result.append(2 * result[-1])
        return result[-1]
