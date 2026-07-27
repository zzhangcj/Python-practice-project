from typing import List

"""
给你一个整数数组 nums ，数组中的元素 互不相同 。
返回该数组所有可能的子集（幂集）。
解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。
"""
#1.多叉树解法（要求掌握）
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        path=[]
        res=[]
        n=len(nums)

        def backtrack(start_index):
            res.append(path.copy())

            for i in range(start_index,n):
                path.append(nums[i])
                backtrack(i+1)
                path.pop()

        backtrack(0)
        return res

"""
为什么这里直接res.append(path.copy())
组合/全排列：只有满足长度条件才收集答案；
子集：path每一种状态都是有效子集，进入backtrack立刻收集path
"""


#2.选还是不选的二叉树解法（了解）
class Solution2:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        path=[]
        res=[]
        n=len(nums)

        def dfs(i): # i是一个指针
            if i>=n: #指针越位即到达叶子节点了，直接添加
                res.append(path.copy())

            #情况1：选择
            path.append(nums[i])
            #递归
            dfs(i+1)
            #回溯
            path.pop()
            #情况2：不选
            dfs(i+1)

        dfs(0)
        return res

"""
1、为什么方法2不用for循环
解法 1（多叉树、带 for+start_index）
循环 for i from start_index：每一层选择「接下来选哪一个数字」
例如 nums=[1,2,3]
第一层可选：1 / 2 / 3；天然保证只往后选，不会重复子集。

解法 2（二叉树、选 / 不选模型）
没有 for！递归参数 i 代表：当前正在处理第 i 号数字
对每一个数字，只有两条分支：选它 ｜ 不选它
二叉树，只有两条路，不需要循环遍历候选

2、选、不选两段代码，是不是每次递归都会全部执行？
✅ 是的，正常流程两条分支都会执行

3.关键
（多叉树 for + start_index）
👉 在每一层节点收集（树上所有节点都是有效子集）
（二叉树选 / 不选）
👉 只在最底部叶子节点收集
"""