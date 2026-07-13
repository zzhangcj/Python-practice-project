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


"""
看到要求最小的子数组（连续的） --> 想到滑动窗口

滑动窗口/快慢指针
关键：当不满足条件的时候，快指针向前探路；当满足条件的时候，慢指针开始起步

注意：适用于数列元素都是正数
这道题数组如果出现负数，则不适用
"""









