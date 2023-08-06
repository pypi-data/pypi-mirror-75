class Solution:
    def uniquePaths(self, m, n):
        # dmap[m][n] 从起点到坐标(m,n)的路径数目
        dmap = [[0] * n for _ in range(m)]
        # 因为只能下/右，到“左边上边”的任意位置的路径数量，只能是1
        for i in range(m):
            dmap[i][0] = 1
        for j in range(n):
            dmap[0][j] = 1
        # 到非“左边上边”坐标上点的路径数
        for i in range(1, m):
            for j in range(1, n):
                # 从起点到坐标(i,j)的路径数目 = 从起点到(i,j)上边点(i-1,j)的路径数 + 从起点到(i,j)左边点(i,j-1)的路径数
                dmap[i][j] = dmap[i-1][j] + dmap[i][j-1]
        return dmap[m-1][n-1]
