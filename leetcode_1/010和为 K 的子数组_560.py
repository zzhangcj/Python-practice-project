from typing import List
'''
1.看到子数组，联想004，209题的滑动窗口，但这道题不能用这个方法解决，为什么？
滑动窗口的前提是数组元素都是单调的（要么全正，要么全负）

2.这道题使用前缀和的方法解题
按照这个思路，如何使用preSum数组呢？
---> 如果要求的子数组为[i,j]，则满足preSum[j]-preSum[i]=k
联想002两数之和_1 -->other = target - item --> 和为定值
而这里是差为定值

'''


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        preSum=[0]*(len(nums)+1)
        for i in range(len(nums)):
            preSum[i+1]=preSum[i]+nums[i]

        cache = {} #注意：这个字典记录某些值出现了几次
        count=0

        for i,item in enumerate(preSum):
            other = item -k
            if other in cache:
                count+=cache[other] #当前前缀和可与前面cache内所有other各组成一段合法子数组
            cache[item]=cache.get(item,0)+1
            # 计算other出现的次数，对应存在符合需求的子数组个数
        return count

"""
cache.get(item, 0)：
如果字典 cache 里已经有键 item → 返回它对应的值（出现次数）
如果字典里没有 item → 返回默认值 0

总结：
核心公式：preSum[i] - preSum[j] = k 等价于 preSum[j] = preSum[i] - k
1. preSum[i]是当前遍历到的前缀和item，other=item-k就是我们要找的preSum[j]
2. 明白这个cache字典存的是什么：只存【当前i左侧】所有前缀和，key=前缀和数值，value=该数值出现次数
对应代码cache[item]=cache.get(item,0)+1
3. count += cache[other]：每一个历史出现过的other，都能和当前item凑出一段和为k的子数组，全部累加
4. 顺序必须先查cache、再更新cache：防止匹配到自身，避免统计空数组
5. 原理等价排列组合的原理（C,即n个里面选2个）：每新增一个相同前缀和，新增配对数=历史已存在的个数，累加得到总子数组数量
"""