class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def zigzagLevelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        # level order
        if root is None:
            return []
        q = [[root]]
        temp = []
        while q:
            level=q.pop(0)
            record = []
            for node in level:
                temp.append(node.val)
                if node.left:
                    record.append(node.left)
                if node.right:
                    record.append(node.right)
            if record:
                q.append(record)
        # zigzag order
        res = []
        for index, level in enumerate(temp):
            if index % 2 == 0:
                res.append(temp)
            else:
                res.append(temp[::-1])
        return res
