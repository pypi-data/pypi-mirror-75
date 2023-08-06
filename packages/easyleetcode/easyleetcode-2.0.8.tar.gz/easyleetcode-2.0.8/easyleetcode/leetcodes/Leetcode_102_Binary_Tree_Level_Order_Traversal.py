class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    # 借助队列
    def levelOrder(self, root):
        res = []
        if not root: return res

        q = [root]
        while q != []:
            rs = []
            size=len(q)
            for i in range(size):
                first = q[0]
                q.remove(first)
                rs.append(first.val)
                if first.left:
                    q.append(first.left)

                if first.right:
                    q.append(first.right)
            res.append(rs)
        print(res)
