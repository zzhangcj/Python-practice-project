from typing import List
"""
给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素
元素的顺序可能发生改变。然后返回 nums 中与 val 不同的元素的数量。

假设 nums 中不等于 val 的元素数量为 k，要通过此题，您需要执行以下操作：

更改 nums 数组，使 nums 的前 k 个元素包含不等于 val 的元素
nums 的其余元素和 nums 的大小并不重要。
返回 k。
"""
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        i=0
        while i<len(nums):
            if nums[i]==val:
                nums.pop(i)
            else:
                i+=1
        return len(nums)

'''
1、为什么这么写？
n = len(nums)   # 只算一次，存的是【最开始的数组长度】
while i < n:

n = len(nums) 只在最开头执行一次，是固定不变的数字。
但是 pop() 会真实把数组变短，len(nums) 在循环过程中越来越小，而 n 还是最初的大数字

2、为什么要if else，即pop操作后，i不变
nums.pop(i)：不会留下空位！后面元素全部向前移动补齐，列表长度会直接‑1
所以pop (i) 之后 i 不增加，留在原地继续检查新挪过来的元素；
'''

##2.快慢指针
class Solution2:
    def removeElement(self, nums: List[int], val: int) -> int:
        fast=slow=0
        for fast in range(len(nums)):
            # if nums[fast]==val:
            #     pass
            # else:
            #     nums[slow]=nums[fast]
            #     slow+=1
            if nums[fast]!=val:
                nums[slow]=nums[fast]
                slow+=1
        return slow

"""
不做删除，直接把不等于 val 的元素往前覆盖，最后返回 k
"""