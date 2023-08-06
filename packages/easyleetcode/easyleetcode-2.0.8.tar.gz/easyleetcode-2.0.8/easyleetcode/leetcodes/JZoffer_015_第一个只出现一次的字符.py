
class Solution:
    def FirstNotRepeatingChar(self, s):
        if len(s) == 0:
            return -1
        for i in range(len(s)):
            if s.count(s[i]) == 1:
                return i
        return -1


class Solution:
    def FirstNotRepeatingChar(self, s):
        # 建立哈希表,有256个字符，于是创建一个长度为256的列表
        ls = [0] * 256
        # 遍历字符串,下标为ASCII值,值为次数
        for i in s:
            ls[ord(i)] += 1  # ord()函数以一个字符作为参数，返回对应的ASCII数值
        for j in s:
            if ls[ord(j)] == 1:
                return s.index(j)
                break
        return -1
