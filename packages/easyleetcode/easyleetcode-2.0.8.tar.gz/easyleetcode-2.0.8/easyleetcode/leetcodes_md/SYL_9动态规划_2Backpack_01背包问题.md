# SYL_9动态规划_2Backpack_01背包问题

```

Given n items with size
A_i, an integer m denotes the size of a backpack. How full you can fill this backpack?

Example
If we have 4 items with size [2, 3, 5, 7], the backpack size is 11,

we can select [2, 3, 5], so that the max size we can fill this backpack is 10.

If the backpack size is 12. we can select [2, 3, 7] so that we can fulfill the backpack.

You function should return the max size we can fill in the given backpack.

Note
You can not divide any item into small pieces.

Challenge
O(n x m) time and O(m) memory.
O(n x m) memory is also acceptable if you do not know how to optimize memory.


本题是典型的01背包问题，每种类型的物品最多只能选择一件。
题中可以将背包的 size 理解为传统背包中的重量；题目问的是能达到的最大 size, 故可将每个背包的 size 类比为传统背包中的价值。

考虑到数组索引从0开始，故定义状态bp[i + 1][j]为 ：选数组中前i个物品，选出重量不超过j时，的最大总价值。
状态转移方程则为分 A[i] > j 与否两种情况考虑。

初始化均为0，相当于没有放任何物品。

分为两种情况
当前背包最大容量小于物品的重量，可容纳的最大重量是dp[i-1][j]
当前背包最大容量小于物品重量，可容纳的最大重量是max(dp[i-1][j],dp[i-1][j-A[i]+A[i])

```