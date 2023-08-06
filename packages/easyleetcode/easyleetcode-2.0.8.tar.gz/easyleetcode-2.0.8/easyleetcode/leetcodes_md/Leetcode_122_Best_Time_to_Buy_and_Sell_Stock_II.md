# L 122 Best Time to Buy and Sell Stock II
 
```
Say you have an array for
which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit.
You may complete as many transactions as you like
(ie, buy one and sell one share of the stock multiple times).
However, you may not engage in multiple transactions at the same time
(ie, you must sell the stock before you buy again).

Example
Given an example [2,1,2,0,1], return 2

卖股票系列之二，允许进行多次交易，但是不允许同时进行多笔交易

计算所有连续波谷波峰的差值之和。
可以把数组看成时间序列，只需要计算相邻序列的差值即可，只累加大于0的差值。
```