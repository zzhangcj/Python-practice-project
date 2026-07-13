from typing import List

#1.暴力破解
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i,item in enumerate(nums):
            for j in range(i+1,len(nums)):
                post = nums[j]
                if item + post ==target:
                    return [i,j]

#enumerate(可迭代对象, start=0)
# start：索引起始数字，默认从 0 开始；
# 每次循环返回 (索引, 元素) 二元组

# nums = [2,7,11,15]
# for i, item in enumerate(nums):
#     print(i, item)

# 0 2
# 1 7
# 2 11
# 3 15


#2.哈希表（在python里就是字典）
class Solution2:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        cache = {} #cache 缓存
        for i,item in enumerate(nums):
            cache[item]=i

        for i,item in enumerate(nums):
            other = target - item
            if other in cache and cache[other] != i:
                return [i,cache[other]]

#3.最标准 (进一步哈希表)
class Solution3:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        cache={}
        for i,item in enumerate(nums):
            other = target - item
            if other in cache:
                return [i,cache[other]]
            cache[item] = i

#字典 dict 没有 append 方法
# 新增 / 修改键值统一语法：
# 字典[key] = 值
# 如果 key 不存在：新增一组键值对；
# 如果 key 已经存在：覆盖原来的 value


'''
当需要记忆功能的时候：
第一个想到---哈希表
哈希表的复杂度为O(1)

other in 字典 只判断 key，不判断 value

方法1：两层循环嵌套，时间复杂度为O(n^2)
方法2：单层两个循环，时间复杂度为O(2n) --> O(n) 
方法3：仅一层循环，循环 n 次，每次循环内查询、插入字典都是平均 O(1),时间复杂度为O(n)
'''









