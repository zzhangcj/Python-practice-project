from typing import List

#1.直接遍历
class NumArray:

    def __init__(self, nums: List[int]):
        self.nums=nums
        print(self.nums)

    def sumRange(self, left: int, right: int) -> int:
        my_sum=0
        for i in range(left,right+1):
            my_sum+=self.nums[i]
        return my_sum

# 2.前缀和     #能以常数级别的复杂度快速计算区间的和
class NumArray2:

    def __init__(self, nums: List[int]):
        self.preSum=[0]*(len(nums)+1) #这里+1，是因为前缀和第0位表示前0个元素的和为0，多了一个开头
        for i in range(len(nums)):
            self.preSum[i+1]=self.preSum[i]+nums[i]

    def sumRange(self, left: int, right: int) -> int:
        return self.preSum[right+1]-self.preSum[left]





if __name__ == '__main__':
    a=NumArray([-2, 0, 3, -5, 2, -1])
    a.sumRange(0,2)
# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)