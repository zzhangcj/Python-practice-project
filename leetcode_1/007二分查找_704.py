from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums)
        #为什么右指针不-1？ --> 区间要左闭右开
        mid = (left + right)//2
        while left < right:
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1 #为什么要加1？ --> mid这个位置已经排除了
            elif nums[mid] > target:
                right = mid #为什么这里不用加1？ -->区间左闭右开，右指针过来取不到mid

            mid = (left + right)//2

        return -1 #当while循环条件不满足，就是说target不在里面

"""
注意elif 的条件，target是和nums[mid]在比较，而不是mid
mid是数组下标，确定位置的，target是值，和数组元素进行比较
"""











#注意：二分查找要求是排好序的