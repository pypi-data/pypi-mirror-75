class Solution(object):

    def uniquePathsWithObstacles(self, obstacleGrid):
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        if m == 0:
            return 0
        # 从下往上的遍历思路
        dmap = [[0] * (n + 1) for _ in range(m + 1)]
        # 从(m-1,n)到(m,n)的路径数量=1
        dmap[m - 1][n] = 1
        for i in range(m - 1, -1, -1):
            for j in  range(n - 1, -1, -1):
                # 遇到“障碍”，到此坐标的路径数量“归零”
                if obstacleGrid[i][j] == 1:
                    dmap[i][j] = 0
                else:
                    # 否则和Unique Paths“类似”，从(i,j)到(m,n)的路径数量 = 从(i,j)下面(i,j+1)到(m,n)的路径数量 + 从(i,j)右面(i+1,j)到(m,n)的路径数量
                    dmap[i][j] = dmap[i][j + 1] + dmap[i + 1][j]
        return dmap[0][0]