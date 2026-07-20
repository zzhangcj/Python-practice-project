from typing import Optional
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


#1.快慢指针
"""
关键的思路：
设A为 head-->环入口 两节点之间的距离；
B为 环入口 --> slow和fast相遇的节点 这两个节点间距离
C为 slow和fast相遇的节点 --> 环入口 这两个节点间的距离
因此链总长为A + B + C
环的总长为 B + C

慢指针slow走的距离： A+B
快指针fast走的距离： A+B+n(B+C)
由于移速是两倍关系-->移动距离也是两倍关系
所以： 2(A+B) = A+B+n(B+C) --> A+B = n(B+C)
因为这道题是找环入口，则要求A --> A = (n-1)(B+C)+C

总结上面的思路，可以知道：
设fast和slow的相遇点为M,指针x从起点head开始移动，指针y从M开始移动，移动速度相同为1
最终x，y会在环的入口节点相遇
"""
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head
        fast = head
        while fast and fast.next: #等价于fast != None and fast.next != None
            slow=slow.next
            fast=fast.next.next

            if slow==fast: #如果有环，这里可以设指针x和y了
                x=head
                y=slow
                while x!=y:
                    x=x.next
                    y=y.next
                return x
        #没有环的情况
        return None

#2.哈希表解法
class Solution1:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        seen=set()
        cur=head
        while cur:
            if cur in seen:
                return cur
            seen.add(cur)
            cur=cur.next
        #没有环，则返回None
        return None

"""
为什么这样不行
        while cur:
            if cur not in seen:
                seen.add(cur)
                cur=cur.next
            return cur

1.return cur 在while循环里面，和if平级       
举带环链表 1 → 2 → 3 → 2        
cur=1，不在集合 → add 1，cur=2-->直接return cur-->函数提前结束

2.return cur 在while循环外，和while平级 
        while cur:
            if cur not in seen:
                seen.add(cur)
                cur=cur.next
        return cur
（1）cur=1，不在集合 → add，cur=2
（2）cur=2，不在集合 → add，cur=3
（3）cur=3，不在集合 → add，cur=2
（4）cur=2，已经在集合里，if 条件不成立：
不执行 add，cur 不会更新，依旧等于节点 2
一轮 while 循环结束，回到循环开头 while cur --> cur 不为空，再次进入循环
（5）重复第（4）步，永远卡在 cur=2，无限循环，永远到不了循环外的 return cur


正确逻辑：先判断当前节点是否重复，重复立刻 return；不重复再存入集合、后移指针
"""

