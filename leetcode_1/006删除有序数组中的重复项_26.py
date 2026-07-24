from typing import List
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

write+=1
nums[write]=nums[read]
这一步会把新的不重复数字覆盖到数组前面的空位，直接原地更新数组

输入 nums=[0,0,1,1,1,2,2,3,3,4]
循环结束后数组变为 [0,1,2,3,4,1,1,2,3,4]
write=4，返回5，判题器只看前 5 位[0,1,2,3,4]

套快慢指针代码，给无序数组会直接失效
失效原因：算法依赖「有序数组重复元素相邻」这个前提
代码判断逻辑只有一句：if nums[read] == nums[write]
它只对比当前遍历元素 和 最后保存的唯一元素，无法识别隔了很多数字的重复值
"""

'''
这道删除重复元素的题为什么不能把 

write+=1

nums [write]=nums [read] 写反了?

write 当前指向最后一个有效位置
新的不重复数字，要存到 write 的下一格
--> 保证nums[0,write+1]里面都是写好的没有重复元素的，所以新的元素得存nums[write+1]
所以必须先 write +=1 腾出空位，再写入新值
'''

#2.无序数组去重
def removeDuplicates(nums):
    write = 0
    seen = set()
    for read in range(len(nums)):
        if nums[read] not in seen:
            seen.add(nums[read])
            nums[write] = nums[read]
            write += 1
    return write

if __name__ == '__main__':
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = removeDuplicates(nums)
    print("不重复的元素个数：",res)
    print("去重后的数组：",nums[:res])

#3.哈希表（这里是一个思路，单这道题不推荐）
"""
注意：哈希表主要是记忆功能，看目前的元素在以往有没有出现过
而这道题是排好序了
"""
