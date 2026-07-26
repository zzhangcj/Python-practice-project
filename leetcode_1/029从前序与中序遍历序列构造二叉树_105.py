"""
给定两个整数数组 preorder 和 inorder
其中 preorder 是二叉树的先序遍历， inorder 是同一棵树的中序遍历
请构造二叉树并返回其根节点
"""
from typing import Optional,List

from pandas.conftest import index


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


#1.正常解法
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None

        root_val=preorder[0]
        root=TreeNode(val=root_val)

        root_idx=inorder.index(root_val)

        root.left=self.buildTree(preorder[1:root_idx+1],inorder[:root_idx])
        root.right=self.buildTree(preorder[root_idx+1:],inorder[root_idx+1:])

        return root

'''
核心规则
preorder：根 → 左 → 右 ---→ preorder[0]永远是当前根
inorder：左 → 根 → 右
在inorder找到根下标root_idx
左子树节点总数 = root_idx

切片规则,注意是左闭右开

对于中序遍历，root_idx左边是左子树，右边为右子树
inorder[:root_idx] → 左子树节点集合
inorder[root_idx+1:] → 右子树节点集合

对于前序遍历，除开第一个根节点preorder[0]-->左子树切片从1开始
-->区间[1 : 1 + root_idx)里面为左子树-->[1 + root_idx : ]为右子树
左子树preorder区间：preorder[1 : 1 + root_idx]
右子树preorder区间：preorder[1 + root_idx : ]

递归终止条件：数组为空
if not preorder: return None
'''
"""
1. 这个函数在利用buildTree来创建一个个子树TreeNode(val,left,right)
所以函数的思路结构就是
先找到root.val --> 创建root.left --> 创建root.right

2.创建好了TreeNode利用递归回到根节点-->递归的每一次减少相当于拼接这些子树

3.为什么是if not preorder 而不是 if not preorder or not inorder
因为两个序列的元素个数是一样的，如果preorder为空列表，则inorder也是空列表

4. 列表.index(x) 函数
查找元素 x 在列表中第一次出现的下标
返回值：元素对应的下标 int
index() 是线性遍历查找 -->时间复杂度O (n)
"""


#哈希表解法
class Solution1:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # 预处理哈希映射：值 -> 在中序数组中的下标
        val_to_idx = {val: i for i, val in enumerate(inorder)}

        def dfs(pre_l, pre_r, in_l, in_r):
            """
            pre_l,pre_r：前序数组当前区间 [pre_l, pre_r] 闭区间
            in_l,in_r：中序数组当前区间 [in_l, in_r] 闭区间
            """
            # 区间没有元素，递归终止
            if pre_l > pre_r:
                return None

            # 前序区间第一个元素 = 当前根
            root_val = preorder[pre_l]
            root = TreeNode(root_val)

            # O(1)拿到根在中序的下标
            root_idx = val_to_idx[root_val]
            # 左子树一共有多少个节点
            left_size = root_idx - in_l

            # 构造左子树
            # 前序：根后第一个位置 ~ 根后+左子树数量
            # 中序：in_l ~ root_idx -1
            root.left = dfs(pre_l + 1, pre_l + left_size, in_l, root_idx - 1)
            # 构造右子树
            # 前序：pre_l+left_size+1 ~ pre_r
            # 中序：root_idx+1 ~ in_r
            root.right = dfs(pre_l + left_size + 1, pre_r, root_idx + 1, in_r)
            return root

        return dfs(0, len(preorder) - 1, 0, len(inorder) - 1)
"""
1. 预处理哈希表
val_to_idx = {val:i for i, val in enumerate(inorder)}
一次性遍历 inorder，记录每个数值对应的下标。
例子：inorder=[9,3,15,20,7]
val_to_idx = {9:0, 3:1, 15:2, 20:3, 7:4}
后续任意值，直接 val_to_idx[root_val] 获取下标，不用循环查找。

2. dfs 参数含义（重中之重）
def dfs(pre_l, pre_r, in_l, in_r):
[pre_l, pre_r]：当前子树对应的前序区间（闭区间）
[in_l, in_r]：当前子树对应的中序区间（闭区间）

3. 递归终止条件
if pre_l > pre_r:
    return None
区间左边界超过右边界，代表没有节点，返回空。
原始写法 if not preorder: 等价功能，只是换成下标判断。

4. 创建根节点
root_val = preorder[pre_l]
root = TreeNode(root_val)
前序区间最左侧永远是当前子树根。

5. 获取根下标 + 计算左子树节点数量
root_idx = val_to_idx[root_val]
left_size = root_idx - in_l
root_idx：根在中序数组的位置
left_size：左子树一共有多少个节点


6. 左子树递归参数
root.left = dfs(pre_l+1, pre_l + left_size, in_l, root_idx - 1)
前序区间：
起点 pre_l+1：跳过根
终点 pre_l + left_size：取连续 left_size 个节点（全部左子树）
中序区间：in_l ~ root_idx-1（根左边全部节点）

7. 右子树递归参数
root.right = dfs(pre_l + left_size + 1, pre_r, root_idx + 1, in_r)
前序区间：左子树结束位置的下一个，一直到区间末尾
中序区间：root_idx+1 ~ in_r（根右边全部节点）
"""

"""一些问题
1.为什么哈希表只用中序数组 inorder构建？
我们的分割逻辑依赖：
在中序数组找到根的位置 root_idx
inorder[in_l : root_idx] = 左子树节点
inorder[root_idx+1 : in_r] = 右子树节点
关键点：
前序数组功能：定位根节点（preorder [pre_l] 就是根）
中序数组功能：分割左右子树，必须知道根在中序的下标
👉 所以我们需要快速查询：根节点的值 → 它在 inorder 中的下标，因此遍历 inorder 建哈希

2.方法1用区间，这里用指针，怎么理解边界控制的细节？
切片 preorder[a:b]Python语法固定：左闭右开 [a,b)

dfs(pre_l,pre_r)指针参数 --> 人为约定闭区间 [pre_l,pre_r]
选用闭区间目的：边界判断简单，终止条件 pre_l > pre_r 清晰，减少+1、-1失误

"""