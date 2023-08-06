# L 097 Interleaving String
 
--- 
 
``` 
Given three strings: s1, s2, s3,
determine whether s3 is formed by the interleaving of s1 and s2.

Example
For s1 = "aabcc", s2 = "dbbca"

When s3 = "aadbbcbcac", return true.
When s3 = "aadbbbaccc", return false.
Challenge
O(n2) time or better

 s3 是否由 s1 和 s2 交叉构成，不允许跳着从 s1 和 s2 挑选字符
 ```