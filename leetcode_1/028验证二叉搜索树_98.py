"""
给你一个二叉树的根节点 root ，判断其是否是一个有效的二叉搜索树。

有效 二叉搜索树定义如下：

节点的左子树只包含 严格小于 当前节点的数。
节点的右子树只包含 严格大于 当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。

"""
from typing import Optional,List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


#1.最自然而然的解法（不推荐，但是这个方法思路要掌握）
class Solution1:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(node:TreeNode,max_limit,min_limit):
            if node is None:
                return True

            left_BST=dfs(node.left,min_limit,node.val)
            right_BST=dfs(node.right,node.val,max_limit)

            if left_BST and right_BST and min_limit<node.val<max_limit:
                return True
            return False
        return dfs(root,float("-inf"),float("inf"))



"""
1、判断条件
if left_BST and right_BST and min_limit<node.val<max_limit:
对应上面对于二叉搜索数的定义：左右子树都满足二叉搜索树，同时自己也得满足

2、是不是后序遍历？
遍历顺序 ≠ 后序遍历
后序遍历定义：左 → 右 → 处理当前节点
单看执行顺序：
递归左子树
递归右子树
判断当前节点条件
👉 执行时序确实符合「左、右、自己」，时序上像后序
⚠️但是！ --> 二叉搜索树约束校验的本质不是依靠遍历顺序，而是上下界传递！


3.总结这个解法
不推荐，先递归子树，返回后校验当前节点
缺陷：节点不合法时，依然会完整遍历左右子树，无法提前剪枝（即返回False）
"""

#2.用先序校验的思想（推荐，要掌握，后面有更优化的版本）
class Solution2:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(node:TreeNode,min_limit,max_limit):
            if not node:
                return True

            if node.val>=max_limit or node.val<=min_limit:
                return False

            left_is_BST=dfs(node.left,min_limit,node.val)
            right_is_BST=dfs(node.right,node.val,max_limit)

            return left_is_BST and right_is_BST

        return dfs(root,float("-inf"),float("inf"))

"""
1.
return left_is_BST and right_is_BST
等价于
if left_is_BST and right_is_BST:
    return True
return False


2. if node.val>=max_limit or node.val<=min_limit: return False
判断条件放在递归调用操作的前面，这个思路的核心就是，走到当前节点，立刻检查本节点数值是否越界。一旦违规直接剪枝

3.借助这个思想进一步优化代码： 如果当前节点合适，看左节点，左节点不合适直接剪枝，合适再看右节点
left_is_BST=dfs(node.left,min_limit,node.val)
if not left_is_BST:
    return False

right_is_BST=dfs(node.right,node.val,max_limit)
if not right_is_BST:
    return False
"""
#3. 优化最终版本(必须掌握)
class Solution3:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(node:TreeNode,min_limit,max_limit):
            if not node:
                return True

            if node.val>=max_limit or node.val<=min_limit:
                return False

            left_is_BST = dfs(node.left, min_limit, node.val)
            if not left_is_BST:
                return False

            right_is_BST = dfs(node.right, node.val, max_limit)
            if not right_is_BST:
                return False

            return True

        return dfs(root,float("-inf"),float("inf"))


#3.中序遍历
"""
前序和后序的思想都做过一遍了，那中序的思想呢？
-->二叉搜索树天然满足：中序遍历的结果是递增的
"""
class Solution4:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        pre=float("-inf")
        def inorder(node:Optional[TreeNode])->bool:
            if not node:
                return True

            nonlocal pre

            left_is_best=inorder(node.left)

            if pre >= node.val:
                return False
            pre=node.val

            right_is_best=inorder(node.right)

            return left_is_best and right_is_best

        return inorder(root)

"""
1. 为什么 pre = float("-inf")
BST 中序要求严格递增。
第一个遍历到的节点没有前驱，要保证 -∞ < 首个节点值，判定自动通过。


2. 为什么 nonlocal pre
pre 定义在外层函数；
inorder() 内层函数修改外层变量；
Python 规则：不加nonlocal，会被当成函数内局部变量，运行报错。
只读变量不需要 nonlocal，写修改必须加

3.优先级
Solution3（带显式提前剪枝上下界先序）
Solution2（and 简写上下界先序）
Solution4（中序递归）
Solution1（无剪枝后序校验版本）
"""