from typing import List
"""给定一个不含重复数字的数组 nums
返回其 所有可能的全排列 。你可以 按任意顺序 返回答案"""


#1.常规解法
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        path=[]
        res=[]
        n=len(nums)
        def backtrack():
            if len(path)==n:
                res.append(path.copy())
                return

            for i in range(n):
                if nums[i] in path:
                    continue

                path.append(nums[i])
                backtrack()
                path.pop()

        backtrack()
        return res

"""
1.为什么path可以写在外面，而不是作为参数传入回溯函数
（1）path 是外层变量，所有递归共享同一个列表。
全程只有唯一一份 path，依靠append()与pop()原地修改、回溯撤销。
✅ 不需要传参，内层函数直接访问外层 path

（2）这里修改的是列表内部元素，没有重新赋值path = xxx，所以不需要 nonlocal。
如果写path = []在内层重新赋值，才需要 nonlocal

2.这里为什么start_index参数也不用写？
组合：从 [1,2,3,4] 选 2 个数
要求：[1,2] 和 [2,1] 算同一种答案，只保留一份
👉怎么实现避免这种颠倒重复？
规定：只能往后选数字，不能回头选前面的数字
比如选了下标 0 (数字 1)，下一轮只能从下标 1 开始，再也不能访问下标 0。
👉 所以必须引入 start_index，用来标记「下一轮循环从哪个下标启动」

全排列：数组 [1,2,3]，找出全部排列
[1,2,3]、[2,1,3] 是两个不同合法答案！允许调换顺序
也就是说：我们允许回头选取前面下标上的数字
👉 既然允许访问前面下标，而组合里面，start_index 的作用是“禁止回头” ，在这里就失去意义
唯一限制：同一个数字不能在 path 里重复出现
👉 改用 used数组 约束：同一个下标元素不能重复选取
"""


#2.用used数组实现哈希表的作用
class Solution2:
    def permute(self, nums: List[int]) -> List[List[int]]:
        path=[]
        res=[]
        n=len(nums)
        used=[False]*len(nums)
        def backtrack():
            if len(path)==n:
                res.append(path.copy())
                return

            for i in range(n):
                if used[i]:
                    continue

                path.append(nums[i])
                used[i]=True# 标记：这个下标元素已使用
                backtrack()
                path.pop()# 回溯：取消标记
                used[i]=False

        backtrack()
        return res

"""
1.为什么用used数组？
使用used数组的目的是为了优化if nums[i] in path
-->这个操作遍历列表，时间复杂度(O(n)

2.used数组原理
used数组里面存储的是True和False
used = [False] * len(nums)
used[i] 标记：nums [i] 这个下标对应的数字，当前是否已经选进 path 里
used[i] = True → 该数字已经被选用，本轮分支不能再选
used[i] = False → 还没选，可以选取

3.什么时候用used数组
① 全排列类题目（元素不能重复选取）
② nums包含重复数字时，只能依靠下标used数组去重
不适用场景：组合问题（start_index已经限制只能向后选，不需要used）
"""