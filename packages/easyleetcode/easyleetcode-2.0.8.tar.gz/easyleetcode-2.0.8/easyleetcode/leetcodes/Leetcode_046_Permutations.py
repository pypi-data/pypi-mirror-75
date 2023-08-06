
# [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
class Solution:

    def permute(self, nums):
        # DPS with swapping
        res = []
        if len(nums) == 0:
            return res
        self.get_permute(res, nums, 0)
        return res

    def get_permute(self, res, nums, index):
        # 固定前index个值的全排列
        if index == len(nums):
            res.append(list(nums))
            return
        for i in range(index, len(nums)):
            nums[i], nums[index] = nums[index], nums[i]
            # 拿交换后的做permute，固定index + 1个值做全排列
            self.get_permute(res, nums, index + 1)
            # 撤回交换，以备新的交换（回撤）
            nums[i], nums[index] = nums[index], nums[i]

# import itertools
# def permute(nums):
#     return list(itertools.permutations(nums))


if __name__ == "__main__":
    s = Solution()
    print(s.permute([1, 2, 3]))
