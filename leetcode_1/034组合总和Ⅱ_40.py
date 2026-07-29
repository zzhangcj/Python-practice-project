from typing import List

"""给定一个候选人编号的集合 candidates 和一个目标数 target
找出 candidates 中所有可以使数字和为 target 的组合
candidates 中的每个数字在每个组合中只能使用 一次 
注意：解集不能包含重复的组合"""

"""
新东西：如何去重
"""
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        path=[]
        res=[]
        n=len(candidates)
        candidates.sort()

        def backtrack(cur_sum,start_index):
            if cur_sum==target:
                res.append(path.copy())
                return

            if cur_sum>target:
                return

            for i in range(start_index,n):
                if i>start_index and candidates[i]==candidates[i-1]:
                    continue

                path.append(candidates[i])
                backtrack(cur_sum+candidates[i],i+1)
                path.pop()

        backtrack(0,0)
        return res

"""
1. 先搞懂两个前置条件
① candidates.sort()
必须先排序！
作用：把值相等的数字挤到相邻位置，我们才能通过 candidates[i] == candidates[i-1] 判断重复数字。
不排序，相同数字分散各处，无法去重。
② continue 是什么作用
continue：直接跳过本次 for 循环剩下逻辑，进入下一轮i。
⚠️区分：
break → 直接结束整个 for 循环
continue → 只跳过当前 i，下一个 i 继续

2. 条件拆解：i > start_index && candidates[i]==candidates[i-1]
分开两半理解：
条件 A：candidates[i] == candidates[i-1]
当前数字 和 前一个数字值相同 → 遇到重复数字。

条件 B：i > start_index（最容易懵！整个解法最关键重点）
我们先反过来：什么时候 i == start_index？
i == start_index 代表：这一层 for 循环，第一次选这个数字，允许选取。
i > start_index 代表：同一层递归，前面已经选过相同数值的数字了，当前这个重复数字不能再选。
核心一句话：去重是【同一层 for 横向去重】，不是递归纵向去重！

3、如果去掉 i > start_index，只写 if candidates[i] == candidates[i-1]: continue呢？

会纵向和横向同时去重，不加这个情况下
纵向去重是因为当指针 i 和 start_index 相等的时候，candidates [i-1] 如果等于 candidates [i]
会执行 continue，导致纵向这里选择相同的数原本是允许重复的，但这里却被 continue 了
所以需要 i>start_index 来保证去重的时候是在横向选择的过程中选到重复数字，确保 i-1>=start_index

但为什么不是 i-1>=start_index 呢？其实是可以这么写与 i > start_index 逻辑等同，只是后者更规范，大家都这么写
"""