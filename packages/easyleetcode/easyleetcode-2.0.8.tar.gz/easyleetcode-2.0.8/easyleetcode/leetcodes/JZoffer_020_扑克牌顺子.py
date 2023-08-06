
class Solution:
    def IsContinuous(self, numbers):
        if not numbers:
            return False
        numbers.sort()
        zeros = 0
        while numbers[zeros]==0:
            zeros = zeros + 1
        for i in range(zeros,len(numbers)-1):
            if numbers[i+1] == numbers[i] or (numbers[i+1] - numbers[i] - 1) > zeros:
                return False
            else:
                zeros -= (numbers[i+1]-numbers[i]-1)
        return True