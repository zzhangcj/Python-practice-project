from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        slow = 0
        fast = 0
        my_sum = 0
        min_len = float("inf") #无穷大
        while fast < len(nums):
            my_sum += nums[fast]
            while my_sum >= target:
                min_len = min(min_len,fast-slow+1)
                my_sum -= nums[slow]
                slow+=1

            fast+=1

        return min_len if min_len != float("inf") else 0


class Solution1:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        n = len(nums)
        my_sum = 0
        min_len = float("inf")
        for right in range(n):
            my_sum += nums[right]
            while my_sum >= target:
                min_len = min(min_len, right - left + 1)
                my_sum -= nums[left]
                left += 1
        return min_len if min_len != float("inf") else 0


"""
看到要求最小的子数组（连续的） --> 想到滑动窗口

滑动窗口/快慢指针
关键：当不满足条件的时候，快指针向前探路；当满足条件的时候，慢指针开始起步

注意：适用于数列元素都是正数（单调的，或者全是负数）
这道题数组如果出现负数，则不适用
"""

"""
自己写遇到一些问题：
1. for right in range() 会自动遍历，不能搭配手动 right +=1；
而while 循环则能手动控制指针
滑动窗口只用一层 for 控制右指针，while 收缩左指针

2.等价逻辑拆解
for fast in range(n) 底层本质就是：
fast = 0
while fast < n:
    fast = fast + 1

--->for 等价于 while + 手动指针自增

3.什么时候优先用 for，什么时候用 while？
① 固定从头至尾逐个遍历数组 → for 更简洁
像本题，fast 必须一步一步从 0 走到末尾，不会跳步、不会中途停止，用for省去手动写fast += 1，代码更短。
② 需要灵活控制指针（跳跃、中途暂停、回退）→ 外层 while 更灵活
如果后续题目需要：
fast 一次加 2、
满足某个条件就不再右移、
fast 需要往回走
这种场景for做不到，只能用while手动控制fast。

"""








