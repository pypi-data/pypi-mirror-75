
class Solution:
    def __init__(self):
        self.stack = []
        self.minStack = []

    def push(self, node):
        self.stack.append(node)
        if not self.minStack or node < self.minStack[-1]:
            self.minStack.append(node)  # 保存最小元素到栈顶
        else:
            self.minStack.append(self.minStack[-1])

    def pop(self):
        if self.stack:
            self.stack.pop()
            self.minStack.pop()

    def top(self):
        if self.stack:
            return self.stack[-1]
        else:
            return None

    def min(self):
        if self.minStack:
            return self.minStack[-1]
        else:
            return None
