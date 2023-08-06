# L 055 Jump Game
 
```
Given an array of non-negative integers, you are initially positioned at the first index of the array.

Each element in the array represents your maximum jump length at that position.

Determine if you are able to reach the last index.

Example
A = [2,3,1,1,4], return true.
A = [3,2,1,0,4], return false.

State: f[i] 从起点出发能否达到i

从坐标i出发所能到达最远的位置为
f[i] = i + A[i]
如果要到达最终位置，即存在某个i使得
f[i]≥N−1, 而想到达i, 则又需存在某个j
使得f[j]≥i−1. 依此类推直到下标为0.
```