from typing import List

#1.传统方法
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        cache={}
        for i,item in enumerate(numbers):
            other = target - item
            if other in cache:
                return [cache[other]+1,i+1]
            cache[item] = i

if __name__ == '__main__':
    s = Solution()
    res = s.twoSum([2,7,11,15],9)
    print(res)

#改编自002
#return [i,cache[other]] --->  return [cache[other]+1,i+1]
#但是不满足条件：你所设计的解决方案必须只使用常量级的额外空间
#分析空间复杂度：这里最好就是常数级别，最坏就是N

#2.双指针
class Solution2:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers)-1
        while left<right:
            #left < right 保证 index1 < index2，不会取同一个元素
            my_sum = numbers[left] + numbers[right]
            if my_sum == target:
                return [left+1,right+1] #题目要求要下标要从1开始
            elif my_sum >target:
                right-=1
            elif my_sum <target:
                left+=1


"""
总结：

1.看到有序的的排列，要想到--> 指针
2.找两个数 --> 双指针

3.什么时候用for，什么时候用while
for ：循环次数提前已知、固定
while ：循环次数不固定，终止条件由内部逻辑动态决定
"""