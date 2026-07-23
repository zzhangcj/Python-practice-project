"""
给定一个二叉树 root ，返回其最大深度
二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数
"""

from typing import Optional,List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


"""这道题要在收集到所有分支情况以后再返回节点进行判断--->后序遍历"""
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        #边界条件
        if root is None:
            return 0
        #遍历和处理
        left=self.maxDepth(root.left)
        right=self.maxDepth(root.right)

        #返回
        return max(left,right)+1

"""
1.为什么这里是root/前面遍历是node?
因为这里一开始：if root is None
root / node 只是变量名，可以互相替换，不影响逻辑

2.为什么024的遍历中，内部再定义一个函数不用self，而这里要用self？
（1）maxDepth 是类的成员函数（方法）。
在类内部调用自身方法，语法强制要求：self.方法名()
self 代表当前 Solution 实例对象，用来找到这个方法
（2）f() 定义在 preorderTraversal 函数里面，不是 Solution 类的方法，只是普通局部函数。
调用它直接写名字 f()，和 self 没有关系
"""