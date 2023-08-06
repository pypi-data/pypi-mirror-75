class Solution:
    def search(self, A):
        if A is None:
            return -1
        start = 0
        end = len(A) - 1
        mid = 0
        while start + 1 < end:
            mid = start + int((end - start) / 2)
            # 在右边
            if A[mid] < A[end]:
                end = mid
            else:
                # 在左边
                start = mid
        if A[start] < A[end]:
            return A[start]
        else:
            return A[end]

print('<iframe src="//player.bilibili.com/player.html?aid=583841024&bvid=BV18z4y1D7Ya&cid=209622775&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>')

# 从小到大的数组被旋转
# 二分搜索，穷举旋转的时候，mid坐在左、右边情况
s = Solution()
print(s.search([3, 4, 4, 5, 7, 8,1,  2]))
