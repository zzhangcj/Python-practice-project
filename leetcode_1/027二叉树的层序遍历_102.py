"""
给你二叉树的根节点 root ，返回其节点值的 层序遍历 。
（即逐层地，从左到右访问所有节点）。
"""
"""其实就是广度优先遍历"""


"""
层序遍历的时候，读取到一层的信息先存起来，等读了解到下一层什么情况再打印-->先进先出

只要是层序遍历，广度优先遍历-->想到队列

"""

from typing import Optional,List
from collections import deque #导入队列，deque是一个双向链表
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return [] #确保root不是空的

        queue=deque()
        queue.append(root)
        res=[]

        while queue: #当队列不为空，则一直执行
            n=len(queue)
            cur_level=[]
            for i in range(n):
                node=queue.popleft()
                cur_level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            res.append(cur_level)

        return res

"""
1. node=queue.popleft()
表示弹出左边的元素，如果写pop()则会弹出右边的

2，下面的循环，每一次i的变动，队列都会弹出一个元素，并判断是否有孩子节点
    for i in range(n):
        node=queue.popleft()
        cur_level.append(node.val)
        ......
        
3. 关键点：怎么进行分层操作的
while queue:
    n=len(queue) #在每层开始之前，先记录当前队列里【当前这一层所有节点的数量】
    cur_level=[] #因为在while循环里面，每一层的记录结束，都会重新初始化

每进行一次完整的for循环代表完成了这一层的遍历和记录

4.随口一提：广度优先遍历对于解决寻找最短路径问题有优势

"""

