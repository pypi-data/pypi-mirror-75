class Solution(object):


    def edit_distance(self, str1, str2):
        # i x j matrix , 初始化是：i+j次
        edit = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i - 1] == str2[j - 1]:
                    d = 0
                else:
                    d = 1
                edit[i][j] = min([edit[i - 1][j] + 1, edit[i][j - 1] + 1, edit[i - 1][j - 1] + d])
        return edit[len(str1)][len(str2)]

solution = Solution()
print(solution.edit_distance('karma','mart'))

