class Solution:
    # @param A: An integers list.
    # @return: return any of peek positions.
    def findPeak(self, A):
        if not A:
            return -1

        l, r = 0, len(A) - 1
        while l + 1 < r:
            # 取中点位置
            mid = l + int((r - l) / 2)
            # 判断中点位置左右情况
            # 左>中，峰在左
            if A[mid] < A[mid - 1]:
                r = mid
            elif A[mid] < A[mid + 1]:  # 右>中，峰在右
                l = mid
            else:  # 此时的mid比左右元素均大
                return mid
        # 单峰，谁大谁返回
        mid = l if A[l] > A[r] else r
        return mid

print('<iframe src="//player.bilibili.com/player.html?aid=796280508&bvid=BV1MC4y1h7BR&cid=209622032&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>')

s = Solution()
print(s.findPeak([4, 5, 3,2,1]))
