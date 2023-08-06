class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: bool
        """

        if not s:
            return True
        dp = [False] *(len(s)+1)
        dp[0] = True                 # 第一个设置为True
        for i in range(1, len(s)+1):
            for j in range(i):
                # 判断条件，前j个字符能根据词典中的词被成功分词 and s[j:i] 在 wordDict，则：前i个字符可被分词
                if dp[j] and s[j:i] in wordDict:
                    dp[i] = True
                    break
        return dp[-1]

s = "leetcode"
wordDict = ["leet", "code"]

solution = Solution()
print(solution.wordBreak(s,wordDict))
