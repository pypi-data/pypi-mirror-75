# L 139 Word Break
 
```
Given a string s and a dictionary of words dict, determine if s can be
segmented into a space-separated sequence of one or more dictionary words.

For example, given
s = "leetcode",
dict = ["leet", "code"].

Return true because "leetcode" can be segmented as "leet code".

State: f[i] 表示前i个字符能否根据词典中的词被成功分词
Initialization: f[0] = true, 数组长度为字符串长度 + 1，便于处理。
Answer: f[s.length]
```