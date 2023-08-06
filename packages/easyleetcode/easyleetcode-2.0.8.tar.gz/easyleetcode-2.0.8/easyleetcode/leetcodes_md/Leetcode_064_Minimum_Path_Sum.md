# L 064 Minimum Path Sum
 
---

```
Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the sum of all numbers along its path.

Note
You can only move either down or right at any point in time.

题解
State: f[x][y] 从坐标(0,0)走到(x,y)的最短路径和
Function: f[x][y] = (x, y) + min{f[x-1][y], f[x][y-1]}
Initialization: f[0][0] = A[0][0], f[i][0] = sum(0,0 -> i,0), f[0][i] = sum(0,0 -> 0,i)
Answer: f[m-1][n-1]
注意最后返回为f[m-1][n-1]而不是f[m][n].

```