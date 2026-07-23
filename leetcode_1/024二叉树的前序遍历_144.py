"""给你二叉树的根节点 root ，返回它节点值的 前序 遍历"""

"""
二叉树的的三种遍历方式

前序遍历：根 → 左 → 右
中序遍历：左 → 根 → 右
后序遍历：左 → 右 → 根

记忆技巧-->看根的位置：
前序 = 根最先；
中序 = 根在中间；
后序 = 根最后。
"""
"""
做题技巧：
遇到二叉树的题，一定会用递归的方式解决

递归函数的组成，固定套路
1.边界判断
2。遍历操作
3.返回

"""
from typing import Optional,List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#1.前序遍历
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res=[]
        def f(node:Optional[TreeNode]):
            if node is None:
                return
            #中
            res.append(node.val)
            #左
            f(node.left)
            #右
            f(node.right)

        f(root)
        return res

#2.中序遍历-->leetcode94
class Solution1:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res=[]
        def f(node:Optional[TreeNode]):
            if node is None:
                return

            #左
            f(node.left)
            #中
            res.append(node.val)
            #右
            f(node.right)

        f(root)
        return res


#同样的后序遍历-->leetcode145



"""
1.为什么有个return没有返回值？
不带值的 return，等价于 return None
作用：递归终止条件（基线条件）
当 node == None（空节点，没有子树），直接结束当前这一次 f() 函数，回到上一层调用它的地方继续执行

f(A)
    append A.val
    f(A.left)  # 进入左子树
        f(B.left) → 这里node=None，执行return
        # return 结束，回到 f(B)，继续执行后面 f(B.right)
        
2.为什么中间就append，左右就调用函数递归？
中是节点，有值，执行 append；左右是分支，继续递归

append = 处理当前节点；f (child) = 遍历孩子所在的整棵子树

3.补充：系统栈
二叉树递归遍历依托系统调用栈；向下递归时持续压入函数现场，
触发终止条件后逐层回溯，系统栈依次弹出现场继续执行，天然符合栈后进先出特性

"""