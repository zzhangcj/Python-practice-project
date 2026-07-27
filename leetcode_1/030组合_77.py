"""
给定两个整数 n 和 k，返回范围 [1, n] 中所有可能的 k 个数的组合
你可以按 任何顺序 返回答案
"""
from typing import List

#1.多叉树的解法
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        nums=[i for i in range(1,n+1)]
        result=[]

        def backtrack(path,start_index):
            if len(path)==k:
                result.append(path[:])
                return

            for i in range(start_index,len(nums)):
                path.append(nums[i])
                backtrack(path,i+1)
                path.pop()

        backtrack([],0)
        return result

"""
总结（重要）
如果碰到树形结构，无论多叉树还是二叉树，大概递归结构没跑了
如果遇到要求列出所有情况，无论排列组合，子集，字符串分割等题，都要想到回溯算法

1.流程
(1).终止条件：len(path) == k → 拷贝path存入结果，return
(2).for循环 [start_index , len(nums))
    path.append()      # 选择
    backtrack(path,i+1)# 递归，下一轮起点i+1
    path.pop()         # 回溯撤销选择

重点：
result.append(path[:]) 必须拷贝，不能直接append(path)
回溯算法的固定套路：1.选择-->2.递归-->3.回溯撤销选择

2.关键参数

(1) path：是一个列表，用来存放【当前递归分支已经选好的数字】
-->path初始为空列表-[]->一轮循环后变成[一个元素]-->[两元素].....

(2)start_index：本轮循环开始遍历的数组下标，保证只向后选取数字，不回头、不重复


3.path[:] 切片拷贝
(1)复习深浅拷贝
之前学到的是从copy模块里面导入copy，deepcopy
举例数组num=[1, 2, 3, [3, 5, 4]],注意这里列表里面元素有个子列表
浅拷贝后，只会复制外层的容器，拷贝的数组修改内层子数组依旧会影响原数组
深拷贝则是内部嵌套的子数组依旧不受影响

(2)path[:] 近似于 copy.copy(path)   # 浅拷贝
result.append(path)-->不可行
由于这里添加的是path，但是后面path会被修改，导致这里已经放入result的path也会被修改

path[:] → 通过切片，生成【一份全新独立的列表副本】
result.append(path[:])，这里添加的是path的副本，后续改动path对result添加的元素没有影响


"""