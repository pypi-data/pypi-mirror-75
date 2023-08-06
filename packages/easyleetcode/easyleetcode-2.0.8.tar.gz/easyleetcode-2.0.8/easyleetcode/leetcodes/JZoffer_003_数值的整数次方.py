


class Solution:
    def Power(self, base, exponent):
        if exponent == 0: return 1
        if base == 0: return 0
        temp = 1
        if exponent < 0:
            abs_exponent = -exponent
            while abs_exponent > 0:
                temp = temp * base
                abs_exponent = abs_exponent - 1
            return 1 / temp
        while exponent > 0:
            temp = temp * base
            exponent = exponent - 1
        return temp
