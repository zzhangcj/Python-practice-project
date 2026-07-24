from typing import List
# 给你一个未排序的整数数组 nums ，请你找出其中没有出现的最小的正整数。
# 请你实现时间复杂度为 O(n) 并且只使用常数级别额外空间的解决方案。

#1.自然而然的想法
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        i = 1 #正整数从1开始
        while True:
            if i in nums:
                i+=1
            else:
                return i
#结果是超时，因为i每一次跟新都要在nums里面遍历一次-->复杂度O(n*n)

#2.换成集合（哈希表），就能降低复杂度
class Solution2:
    def firstMissingPositive(self, nums: List[int]) -> int:
        num_sets=set(nums)
        i=1
        while True:
            if i in num_sets:
                i=i+1
            else:
                return i

'''
if i in num_set
为什么转换成集合（哈希表）的能将O(n)的复杂度转换为常数级别的复杂度？
（1）list 的 in 是线性遍历 O (n)；set 底层是哈希表，in 是平均常数O(1)
（2）列表底层是连续数组，没有任何快速索引机制：
执行 x in list 时，Python 只能从头逐个遍历对比元素
（3）set底层是哈希表，不靠遍历，靠哈希函数直接定位位置，单次查找几乎不随数组长度变化
'''

#3.原地哈希
class Solution3:
    def firstMissingPositive(self, nums: List[int]) -> int:
        i = 0
        while i<len(nums):
            num=nums[i]
            if i == num-1:#恰好归位
                i=i+1
            else: #位置不对
                if 1<=num<=len(nums) and nums[nums[i]-1]!=nums[i]:
                    nums[num-1],nums[i]=nums[i],nums[num-1]
                else: #没有归位资格的数
                    i+=1

#再次遍历寻找那个值
        for i in range(len(nums)):
            if i==nums[i]-1:
                pass
            else:
                return i+1

#4.原地哈希的优美完整代码
class Solution4:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        i = 0
        while i < n:
            num = nums[i]
            pos = num - 1 #num应该出现的位置
            # 数字合法 且 目标位置不是当前数字，才交换
            if 1 <= num <= n and nums[pos] != num:
                nums[pos], nums[i] = nums[i], nums[pos]
            else: #恰好归位和没有归位资格的，i正常更新
                i += 1
        # 遍历找第一个不匹配的下标
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        # 1~n全部存在，缺失最小正整数是n+1
        return n + 1

'''
1，nums[num-1],nums[i]=nums[i],nums[num-1]
等价于
target = nums[num-1]
nums[num-1]=num
nums[i]=target

注意：写这种交换，尽量不要在[]内进行复杂计算或者嵌套，很可能出错

2，if 1<=num<=len(nums) and nums[nums[i]-1]!=nums[i]
第一个条件判断是否有归位的资格，如果有-->应到num-1位置,即[1,n]
只要 1~n 有缺口，答案一定落在 1~n；
只有 1~n 全部齐全，答案才是 n+1 --->最后才return n+1

第二个判断条件判断要交换位置的两个元素是否相等 --> 不等则交换，否则会陷入死循环
'''





