
class Solution:
    def StrToInt(self, str):
        str = str.strip()
        if not str:
            return 0
        number, flag = 0, 1
        # 符号位的判断是否有正负号
        if str[0] == '-':
            str = str[1:]
            flag = -1
        elif str[0] == '+':
            str = str[1:]
        # 遍历除+，-以外的所有字符，如果遇到非数字，则直接返回0
        for c in str:
            if c >= '0' and c <= '9':
                number = 10 * number + int(c)
            else:
                return 0
        number = flag * number
        return number
