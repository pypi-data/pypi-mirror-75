
class Solution(object):
    def minPathSum(self, grid):
        height = len(grid)
        if height == 0:
            return 0
        width = len(grid[0])
        # height x width
        pathmap = []
        for i in range(height):
            pathmap.append([100000000000] * width)
        pathmap[0][0] = grid[0][0]
        for i in range(height):
            for j in range(width):
                compare = [pathmap[i][j]]
                if i - 1 >= 0:
                    # up
                    compare.append(pathmap[i - 1][j] + grid[i][j])
                if j - 1 >= 0:
                    # left
                    compare.append(pathmap[i][j - 1] + grid[i][j])
                # min choice，得到从i,j走到x,y的最小路径和
                pathmap[i][j] = min(compare)
        return pathmap[-1][-1]