from typing import Optional
"""
给你两个 非空 的链表，表示两个非负的整数。
它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。

请你将两个数相加，并以相同形式返回一个表示和的链表。

你可以假设除了数字 0 之外，这两个数都不会以 0 开头。
"""

#1.我自己写的（有错的）
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if l1 is None:
            return l2
        if l2 is None:
            return l1
        res=ListNode()

        while l1 and l2:
            cur_sum = 0
            cur_sum+=l1.val+l2.val
            if cur_sum >= 10:
                cur_sum -= 10
                l1.next.val+=1
            l1=l1.next
            l2=l2.next
            l1.val = l1.next.val
            l2.val = l2.next.val
            res.val=cur_sum
            res=res.next

        return res

'''
bug1：直接修改原链表 l1.next.val +=1
你把进位直接加到输入链表l1的下一个节点上。
如果l1.next是None（链表已经走到末尾）
执行 l1.next.val +=1 →直接报错 AttributeError

bug2：res=ListNode()，res=res.next
你初始化 res 只有一个节点，res.next 一开始是 None
循环里写res = res.next，第一轮之后 res 就变成None，后续res.val=xxx直接报错

bug3 循环内部两行无意义错误代码
l1.val = l1.next.val
l2.val = l2.next.val
这里强行覆盖 l1、l2 当前节点的值，逻辑完全多余而且错误；
如果l1.next为 None，l1.next.val直接报错

bug4：只处理 l1、l2 同时不为 None 的情况
链表长度可以不一样：比如 l1 长度 3，l2 长度 2
当 l2 走完变成 None，l1 还有节点，你的 while 直接退出，剩余节点完全没有处理

bug5：最高位进位没有处理
cur_sum 每次循环重置为 0，这个本身没问题，但进位没有变量保存
例子 9+9 =18，最后还多出进位1，需要额外新建节点存进位，你的代码完全没有处理

总结核心误区：
❌企图把进位写回输入链表 l1，绝对不可行；
❌不使用哨兵哑结点（即虚拟头节点），操作结果链表逻辑混乱；
❌没有独立变量专门保存进位 carry；
❌没有处理两个链表长度不一致；
❌没有处理循环结束之后，还残留最高进位的场景
'''

#2.优美解法：虚拟头节点
class Solution1:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy=ListNode()
        cur=dummy #cur用来遍历、构建结果链表
        carry=0 #处理进位的

        # 只要还有节点 或者 还有进位，就要继续循环
        while l1 and l2 or carry!=0:
            #没有节点就取0
            v1=l1.val if l1 else 0
            v2=l2.val if l2 else 0

            total=v1+v2+carry
            cur_val=total%10
            carry=total//10

            #新建节点，接到结果链表后面
            cur.next=ListNode(cur_val)
            cur=cur.next

            #原链表指针后移，不为None才移动
            if l1:
                l1=l1.next
            if l2:
                l2=l2.next

        return dummy

"""
✅什么时候必须 / 优先用虚拟头节点
场景：
    1、需要构造一条全新的结果链表，不知道结果链表第一个节点是谁
    2、头节点处于危险情况(头节点可能会被删除)
📝通用模板
# 1. 创建虚拟头结点
dummy = ListNode()
# current / cur：工作指针，用来往后拼接节点
cur = dummy

# 2. while循环处理业务逻辑
while 条件:
    # 选出/生成当前要的节点 node
    cur.next = node   # 拼接到后面
    cur = cur.next    # 工作指针往后移动

# 3. 循环结束，处理剩余尾巴（剩余节点 / 剩余进位）
# 例如合并链表：把剩下的直接接上；两数相加处理最后的进位

# 4. 返回真正的链表头，一定是 dummy.next
return dummy.next

思考流程
做链表题的思考步骤（标准化流程，照着训练，提升细节能力）
以后做链表算法，强制按这 5 步想，不要上来就敲代码。

步骤 1：审题决策
1）输出是全新链表，还是原地修改旧链表？
2）如果生成新链表：结果的第一个节点是否确定？不确定 → 必须用 dummy 虚拟头。

步骤 2：定义全部变量，写清楚每个变量干什么
草稿纸上写：
dummy
cur（构建结果链表的工作指针）
原链表遍历指针 p1,p2
辅助变量（例如 carry 进位）

步骤 3：确定 while 循环条件（重中之重，大部分 bug 出在这里）
合并链表：while list1 and list2，两个都不为空才进入循环；剩下的后面直接接尾巴。
两数相加：while l1 or l2 or carry，只要有一个成立继续循环
循环条件决定什么情况退出循环，退出之后一定还有剩余工作要处理（剩余节点 / 进位）

步骤 4：循环内部逻辑
如果是复用原有节点：cur.next = 选出来的旧节点；原链表指针后移；cur = cur.next
如果要生成新节点：cur.next = ListNode(计算出来的值)；cur = cur.next

步骤 5：循环结束后，处理残余
合并链表：剩下的链表直接接到 cur.next
两数相加：循环条件包含 carry，循环结束无残余

步骤 6：返回结果
用 dummy 的题目：返回dummy.next
"""

