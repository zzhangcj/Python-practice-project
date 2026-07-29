"""
给你一个 无重复元素 的整数数组 candidates 和一个目标整数 target
找出 candidates 中可以使数字和为目标数 target 的 所有 不同组合
并以列表形式返回。你可以按 任意顺序 返回这些组合。
candidates 中的 同一个 数字可以 无限制重复被选取
如果至少一个数字的被选数量不同，则两种组合是不同的。

对于给定的输入，保证和为 target 的不同组合数少于 150 个
"""

from typing import List

"""看到组合--->第一想起回溯算法"""
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res=[]
        path=[]
        n=len(candidates)

        def backtrack(cur_sum,start_index):
            if cur_sum==target:
                res.append(path.copy())
                return

            if cur_sum>target:
                return

            for i in range(start_index,n):
                path.append(candidates[i])
                backtrack(cur_sum+candidates[i],i)
                path.pop()

        backtrack(0,0)
        return res

"""
1、为什么要传参数cur_sum？
如果每一次递归都要计算path所有元素和会很费时间
-->把上层递归的path和的和往内层传递，是一种前缀和的思路

2.为什么要传参数start_index？
因为这是一个组合，需要收缩区间来避免后续选择得到结果和前面选择的结果重复

3.为什么还要一个if cur_sum>target: return？
因为”无限制重复被选取“，如果 cur_sum 已经超过 target
继续叠加元素只会更大，需要及时 return，避免无效递归

2、backtrack(cur_sum+candidates[i],i)
cur_sum+candidates[i]-->前缀和的思路
为什么第二个参数为i，而不是i+1？
因为题干中candidates 中的 同一个 数字可以 无限制重复被选取 
"""

"""
当看到题目给了组合，同时给了一个预算target--->联想到排序

因为上面的算法都是对每一种情况进行了遍历，只是避免了超过target仍然添加元素的情况
数组升序排序后，同一层 for 循环，如果当前candidates[i]+cur_sum>target
后面数字更大，必然也大于 target，无需继续遍历，直接 break 剪枝
-->可以提前剪枝-->怎么提前剪枝？-->排序
"""
class Solution2:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res=[]
        path=[]
        n=len(candidates)
        candidates.sort()

        def backtrack(cur_sum,start_index):
            if cur_sum==target:
                res.append(path.copy())
                return

            if cur_sum>target:
                return

            for i in range(start_index,n):
                if candidates[i]+cur_sum>target:
                    break
                path.append(candidates[i])
                backtrack(cur_sum+candidates[i],i)
                path.pop()

        backtrack(0,0)
        return res

"""
为什么 for 循环内用 break，不能用 return？

break：仅仅跳出当前这一层 for 循环，backtrack函数本身还没结束；循环结束后，函数正常执行完毕，自动回到上一层递归。
return：直接终止整个 backtrack 函数，立刻返回到上层，本层 for 循环剩下所有可能性全部放弃

这里需要的是 当前这一分支搜索结束，即当前层往后不需要再尝试了，但上一层不受影响
--->正常回溯，回到上层--->用break

形象比喻
递归树每一层 = 当前 for 循环
return：直接砍掉整条子树，立刻爬回父节点
break：当前这一层剩下的枝条全部剪掉，但是当前分支到此为止，优雅退回父节点
"""