
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def HasSubtree(self, pRoot1, pRoot2):
        if (pRoot1 == None):
            return False
        if (pRoot2 == None):
            return False
        return (self.dfs(pRoot1, pRoot2) or self.HasSubtree(pRoot1.left, pRoot2) or self.HasSubtree(pRoot1.right,
                                                                                                    pRoot2))

    def dfs(self, R1, R2):
        if (R2 == None):
            return True
        if (R1 == None):
            return False
        if (R1.val != R2.val):
            return False
        return self.dfs(R1.right, R2.right) and self.dfs(R1.left, R2.left)
