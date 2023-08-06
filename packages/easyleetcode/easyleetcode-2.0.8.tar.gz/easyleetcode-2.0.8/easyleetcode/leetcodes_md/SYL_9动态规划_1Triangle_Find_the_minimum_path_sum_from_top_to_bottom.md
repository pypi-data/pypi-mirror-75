# SYL_9动态规划_1Triangle_Find_the_minimum_path_sum_from_top_to_bottom


```

Given a triangle, find the minimum path sum from top to bottom. Each step you may move to adjacent numbers on the row below.

Note
Bonus point if you are able to do this using only O(n) extra space, where n is the total number of rows in the triangle.

Example
For example, given the following triangle

[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
The minimum path sum from top to bottom is 11 (i.e., 2 + 3 + 5 + 1 = 11).
题中要求最短路径和，(每次只能访问下行的相邻元素)，将triangle视为二维坐标。

1：首先考虑最容易想到的方法——递归遍历，逐个累加所有自上而下的路径长度，最后返回这些不同的路径长度的最小值。
由于每个点往下都有2条路径，使用此方法的时间复杂度约为
O(2n)O(2^n)

```