
from functools import cmp_to_key


class Solution:
    def cmp(self, a, b):
        if a + b > b + a:
            return 1
        if a + b < b + a:
            return -1
        else:
            return 0

    def PrintMinNumber(self, numbers):
        if not numbers:
            return ""
        number = [str(x) for x in numbers]
        number.sort(key=cmp_to_key(self.cmp))
        #
        return "".join(number).lstrip('0') or '0'


so = Solution()
# .lstrip('0') or '0'
print(so.PrintMinNumber([0, 32, 321]))
print(so.PrintMinNumber([3, 32, 321]))
