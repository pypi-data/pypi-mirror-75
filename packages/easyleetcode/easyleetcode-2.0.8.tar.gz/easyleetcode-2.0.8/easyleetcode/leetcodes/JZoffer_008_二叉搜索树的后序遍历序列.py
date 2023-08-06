
class Solution:
    def VerifySquenceOfBST(self, sequence):
        if len(sequence) == 0:
            return False
        return self.subVerifySquenceOfBST(sequence)
    def subVerifySquenceOfBST(self, sequence):
        if len(sequence) <= 2:
            return True
        flag = sequence[-1]
        index = 0
        while sequence[index] < flag:
               index += 1
        j = index
        while j < len(sequence)-1:
            if sequence[j] > flag:
                j += 1
            else:
                return False
        return self.subVerifySquenceOfBST(sequence[:index]) and self.subVerifySquenceOfBST(sequence[index:-1])