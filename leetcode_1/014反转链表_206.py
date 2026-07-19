""" 链表基础 """
'''
1. 节点构成（想象为一个圆）
每个 ListNode 节点（圆）包含两部分：
val：节点存储的数值；
.next：节点内部自带箭头，用于连接下一个节点，本质是节点的内置属性。
规则：最后一个节点的 .next = None，代表链表结束。

2. 两种箭头核心区分（记判断口诀：看有没有 .next）
（1）外部指针（单独箭头，变量 head/cur/prev）
没有 .next，的时候，表示这只是一个标签 / 独立箭头，用来标记指向哪一个节点(圆)；
指向目标可随时切换：可以指向任意节点，也可以悬空（= None）；
示例：cur = None、head = 节点1

（2）节点内部连线（A.next，圆之间的箭头 A→B）
带 .next，依附在某个节点上，只能表示「当前节点连向谁」；
只能通过 节点.next = xxx 修改这条连线指向；
示例：cur.next = prev   nxt = cur.next

3. 完整链表如何表示
只需要 1 个外部指针 head;
head 箭头扎在链表第一个节点(圆)上，作为链表入口；
依靠每个节点自带的 .next 内部箭头，串联整条链表；
遍历逻辑：循环执行 head = head.next，让外部指针不断移动到下一个节点；
遍历终止：当 head = None（外部箭头悬空），代表整条链表遍历完毕；

'''


from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

#1.创建新的链表
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur=None
        while head!= None:
            cur=ListNode(head.val,cur)
            head = head.next

        return cur

#2.原地反转
class Solution2:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None  # 保存「前一个节点」
        cur = head   # 当前正在操作的节点
        while cur:
            nxt = cur.next   # 1. 先把下一个节点存起来，防止断链
            cur.next = prev  # 2. 当前节点反向，指向前一个节点
            prev = cur       # 3. prev 往前挪一步（更新为当前节点）
            cur = nxt        # 4. cur 往前挪一步（去原来的下一个节点）
        return prev

#3.递归解法
class Solution3:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 终止条件：空节点 / 到尾节点
        if not head or not head.next:
            return head
        # 递归反转后半段，new_head 是反转后的头
        new_head = self.reverseList(head.next)
        # 反转指针
        head.next.next = head
        head.next = None
        return new_head






"""
1.理解ListNode
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
示例链表 1 → 2 → 3 → None
节点 1：val=1，next = 节点 2
节点 2：val=2，next = 节点 3
节点 3：val=3，next=None（链表结束标记）
head 只是一个变量，存第一个节点的地址，顺着 next 就能走完整条链

当一个变量存的东西只是地址，没有数据 --> 那就是指针

2. 如何理解cur的不断变化
最开始 cur = None：cur 这个标签贴在空上面
cur = ListNode(head.val, cur)：
先执行右边：造一个新节点，新节点的 next 等于赋值前旧的 cur；
再执行等号：移动cur这个外部箭头，指向新节点

所以，这个方法为首插法
外部箭头cur，每一次移动之前，先创造新的ListNode节点，新节点内部属性next是cur移动前指向的节点
"""