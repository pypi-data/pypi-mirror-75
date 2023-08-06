# L 132 Palindrome Partitioning II
 
--- 
 
```

Given a string s, cut s into some substrings such that
every substring is a palindrome.

Return the minimum cuts needed for a palindrome partitioning of s.

Example
For example, given s = "aab",

Return 1 since the palindrome partitioning ["aa","b"] could be produced
using 1 cut.

f[i] 索引i 处时需要的最少切割数
 ```