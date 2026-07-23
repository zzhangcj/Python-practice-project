from typing import Optional,List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        #定义返回值（当前节点子树有p，当前节点子树有q，最近公共祖先x的地址）
        #也就是说（1、先遍历递归 2、当前节点不是p的祖先，当前节点是不是q的祖先，3、找最近公共祖先x的地址）
            def dfs(node):
                if node is None:
                    return False,False,None
                #1、每一个最小的子树都要进行遍历
                left_has_p,left_has_q,left_x=dfs(node.left)
                right_has_p,right_has_q,right_x=dfs(node.right)

                #2、当前最小的一个子树，要么p，q在你的左右，要么你本身就是
                cur_has_p=left_has_p or right_has_p or node==p
                cur_has_q=left_has_q or right_has_q or node==q
                #3、找最近公共祖先x的地址
                cur_x=None #初始化x的值
                if left_x:
                    cur_x=left_x
                elif right_x:
                    cur_x=right_x
                elif cur_has_p and cur_has_q:
                    cur_x=node

                return cur_has_p,cur_has_q,cur_x

            _,_,x=dfs(root)
            return x

"""
一个解题思路，先看你最后要返回什么，先去把返回值定义出来再倒回去思考
 #定义返回值（当前节点子树有p，当前节点子树有q，最近公共祖先x的地址）

dfs 深度优先遍历
"""

#这个思路更优雅简洁
class Solution1:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if not root or root == p or root == q: return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if not left and not right: return # (1).
        if not left: return right # (3).
        if not right: return left # (4).
        return root # (2). if left and right:
"""
递归解析：

1、终止条件：
if not root or root == p or root == q: return root
a.当越过叶节点，则直接返回 null ； -->if not root
b.当 root 等于 p,q ，则直接返回 root ；

2、递推工作：
a.开启递归左子节点，返回值记为 left ；
b.开启递归右子节点，返回值记为 right ；

3.返回值： 根据 left 和 right ，可展开为四种情况；
这里有个关键点：找到p，q之后会往前一个节点返回信息（right,left），根据信息判断-->找到一个节点满足最近公共祖先节点

(1). 当 left 和 right 同时为空 ：
说明 root 的左 / 右子树中都不包含 p,q ，返回 null ；
(2). 当 left 和 right 同时不为空 ：
说明 p,q 分列在 root 的 异侧 （分别在 左 / 右子树），因此 root 为最近公共祖先，返回 root ；
(3). 当 left 为空 ，right 不为空 ：
p,q 都不在 root 的左子树中，直接返回 right 。具体可分为两种情况：

[a]. p,q 其中一个在 root 的 右子树 中，此时 right 指向 p（假设为 p ）；
[b]. p,q 两节点都在 root 的 右子树 中，此时的 right 指向 最近公共祖先节点 ；

(4). 当 left 不为空 ， right 为空 ：与情况 3. 同理；



"""