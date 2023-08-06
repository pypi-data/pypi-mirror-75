class Solution:
    # Traverse without hashmap
    def dfs(self, x, y, sum, triangle):
        '''
        到triangle中的x,y之前，到积累的路径和为sum
        到triangle中的x+1,y/y+1之前，到积累的路径和为sum + triangle[x][y]
        '''
        # 触底了！
        if x == len(triangle):
            # 判断&保留值
            if sum < self.result:
                self.result = sum
            return
        # 要么往下挪，要么往下挪而且往右挪呗？！
        self.dfs(x + 1, y, (sum + triangle[x][y]), triangle)
        self.dfs(x + 1, y + 1, (sum + triangle[x][y]), triangle)

    def minimumTotal1(self, triangle):
        if triangle is None or triangle == []:
            return -1
        self.result = 100000
        self.dfs(0, 0, 0, triangle)
        return self.result


class Solution2:
    # 「分治」
    def dfs(self, x, y, triangle):
        # triangle中，以x,y为起点到最下面，的最小路径和
        if x == len(triangle):
            # 0为第一个有用行，len(triangle)-1为最后一个。x == len(triangle)意味着超出范围了，为0
            return 0
        b = self.dfs(x + 1, y, triangle)
        r = self.dfs(x + 1, y + 1, triangle)
        # 求得triangle中， x,y下，x,y右下为起点的，的最小路径和。
        # 取其中最小的，加上x,y的值，就是以x,y为起点到最下面，，的最小路径和
        return min(b, r) + triangle[x][y]

    def minimumTotal1(self, triangle):
        if triangle is None or triangle == []:
            return -1
        self.result = self.dfs(0, 0, triangle)
        return self.result



if __name__ == '__main__':
    s = Solution()
    triangle = [
        [2],
        [3, 4],
        [6, 5, 7],
        [4, 1, 8, 3]
    ]
    print(s.minimumTotal1(triangle))

    s2 = Solution2()
    print(s2.minimumTotal1(triangle))
