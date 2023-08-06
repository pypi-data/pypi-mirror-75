class Solution(object):
    def twoSum(self, nums, target):
        nums_index = [(v, index) for index, v in enumerate(nums)]
        nums_index.sort()
        begin, end = 0, len(nums) - 1
        while begin < end:
            curr = nums_index[begin][0] + nums_index[end][0]
            if curr == target:
                return [nums_index[begin][1], nums_index[end][1]]
            elif curr < target:
                begin += 1
            else:
                end -= 1

    def twoSum2(self, nums, target):
        hashset = {}
        for i, m in enumerate(nums):
            if target - m not in hashset:
                hashset[m] = i
            else:
                return (hashset[target - m], i)


def run():
    s = Solution()
    print(s.twoSum2([3, 2, 4], 6))



if __name__ == '__main__':
    run()

print('<iframe src="//player.bilibili.com/player.html?aid=841273273&bvid=BV1f54y1i7zg&cid=209615722&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>')
