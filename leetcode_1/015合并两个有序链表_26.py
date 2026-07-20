from typing import Optional

#将两个升序链表合并为一个新的 升序 链表并返回。
#新链表是通过拼接给定的两个链表的所有节点组成的。

#1.虚拟头节点
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy=ListNode()
        current=dummy
        while list1 and list2: #等价于list1!=None and list2!=None
            if list1.val<=list2.val:
                current.next=list1
                list1=list1.next
                current=current.next
            else:
                current.next=list2
                list2=list2.next
                current=current.next

        if list1==None: #因为不知道list1和list2哪个是悬空的，但又只有这两种情况
            current.next=list2
        else:
            current.next=list1

        return dummy.next


"""
什么时候用虚拟头节点呢？

当新链表头节点不确定（要合并两个链表）
头节点处于危险情况(头节点可能会被删除)
"""


