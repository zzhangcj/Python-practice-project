from typing import Optional
'''
题目：
给你一个链表的头节点 head ，判断链表中是否有环。
如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。
注意：pos 不作为参数进行传递 。仅仅是为了标识链表的实际情况。
如果链表中存在环 ，则返回 true 。 否则，返回 false 。
'''

"""
重要的思路：遇到环形指针，首先想到-->快慢指针  即Floyd判圈算法

这道题说了再次到达，如何判断再次到达？-->联想有记忆的哈希表
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
'''
为什么这里的ListNode和前面反转合并的链表不一样？

1.参数数量、默认值不同
环形链表版本：只传 1 个必填参数 x，无默认值，创建节点必须传数值；
next 强制初始为 None，不能在创建时直接指定后继节点。
关键：这里后台会自动连接节点之间原本为None的next，形成环，这一步你看不见
创建写法：node = ListNode(3)

通用的版本：两个参数都带默认值，不传参自动 val=0, next=None；
支持创建时直接绑定下一个节点。
创建写法：node = ListNode(3, next_node)

2.用法功能不同
合并和反转这些操作可能要创建新的链表或者改造原链表，所以给出next属性方便构造
而这里环形链表不需要改造，只需要你来给出一些基于这个环链表的判断
'''

#1.快慢指针(更重要)
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast=head
        slow=head
        while fast and fast.next: #等价于fast != None and fast.next != None
            slow=slow.next
            fast=fast.next.next

            if slow==fast:
                return True
        return False


#2.哈希表解法
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution1:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        seen = set()
        cur = head
        while cur:
            if cur in seen:
                return True
            seen.add(cur)
            cur=cur.next
        return False




