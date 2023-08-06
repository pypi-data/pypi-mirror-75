
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def FindKthToTail(self, head, k):
        p = head;
        for i in range(k):
            if p == None:
                return None
            else:
                p = p.next
        while (p != None):
            p = p.next;
            head = head.next
        return head
