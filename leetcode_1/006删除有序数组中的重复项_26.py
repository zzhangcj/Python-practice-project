#1,快慢指针(读写，有一定记忆功能)
from os import write
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        read = 0
        write = 0
        while read < len(nums):
            if nums[read] == nums[write]:
                read +=1
            else:
                write+=1
                nums[write]=nums[read]
        return write+1

"""
看到原地修改，常数级别空间复杂度，想到这种写指针覆盖的方法
"""


#2.哈希表（这里是一个思路，单这道题不推荐）
"""
注意：哈希表主要是记忆功能，看目前的元素在以往有没有出现过
而这道题是排好序了
"""
