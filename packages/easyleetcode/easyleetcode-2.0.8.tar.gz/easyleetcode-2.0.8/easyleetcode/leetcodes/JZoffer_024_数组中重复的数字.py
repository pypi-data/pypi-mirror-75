
class Solution:
    # 这里要特别注意~找到任意重复的一个值并赋值到duplication[0]
    # 函数返回True/False
    def duplicate(self, numbers, duplication):
        for i in range(len(numbers)):
            while numbers[i] != i:
                m = numbers[i]
                if numbers[m] == numbers[i]:
                    duplication[0] = m
                    return True
                else:
                    numbers[i] = numbers[m]
                    numbers[m] = m
        return False

    
class Solution2:
    # 这里要特别注意~找到任意重复的一个值并赋值到duplication[0]
    # 函数返回True/False
    def duplicate(self, numbers, duplication):
        if(len(numbers)==0):return False
        for i in numbers:
            if numbers.count(i)>1:
                duplication[0] = i
                return True
        return False
