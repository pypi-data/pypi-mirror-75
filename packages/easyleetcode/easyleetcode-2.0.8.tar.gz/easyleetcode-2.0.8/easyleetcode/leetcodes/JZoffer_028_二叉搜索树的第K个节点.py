
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None



class Solution:
    def __init__(self):
        self.my_list = []  # 用于保存中序遍历的序列的结点

    def in_order(self, pRoot):  # 中序遍历二叉树，并把结果保存到my_list中
        if not pRoot:
            return None
        if pRoot.left:
            self.in_order(pRoot.left)
        self.my_list.append(pRoot)
        if pRoot.right:
            self.in_order(pRoot.right)

    def KthNode(self, pRoot, k):
        self.in_order(pRoot)
        if k <= 0 or k > len(self.my_list):  # 越界
            return None
        return self.my_list[k - 1]

    
class Solution2:
    # 返回对应节点TreeNode
    def __init__(self):
        self.count = 0

    def KthNode(self, pRoot, k):
        if (pRoot != None):
            ret = self.KthNode(pRoot.left, k)
            if (ret != None):
                return ret
            self.count = self.count + 1
            if (self.count == k):
                return pRoot
            ret = self.KthNode(pRoot.right, k)
            if (ret != None):
                return ret
        return None
