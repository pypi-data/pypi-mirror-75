class Solution(object):
    def minCut(self, s):
        if not s:
            return 0
        cut = [i - 1 for i in range(1 + len(s))]
        for i in range(1 + len(s)):
            for j in range(i):
                # s[j:i] is palindrome
                if s[j:i] == s[j:i][::-1]:
                    # 如果  0:i部分需要的最少切割数 >  0:j (j<i)部分需要的最少切割数,则更新
                    cut[i] = min(cut[i], 1 + cut[j])
        return cut[-1]

