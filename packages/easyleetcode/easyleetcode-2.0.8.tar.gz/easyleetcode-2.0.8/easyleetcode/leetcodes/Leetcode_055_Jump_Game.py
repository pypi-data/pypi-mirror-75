class Solution(object):
    def canJump(self, nums):
        length = len(nums)
        begin = length - 1
        # 4，3，2，1，0
        for i in reversed(range(length - 1)):
            if i + nums[i] >= begin:
                begin = i
        # begin == 0 : return True
        return not begin