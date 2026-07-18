from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        #如果有空数组则直接返回
        # if not intervals:
        #     return []

        #先排序
        intervals.sort(key=lambda x:x[0])
        #再合并
        res=[]
        i=0
        cur = intervals[i]
        while i+1<len(intervals):
            next=intervals[i+1]
            if cur[1]>=next[0]:
                cur[1]=max(next[1],cur[1])
            else:
                res.append(cur)
                cur=next
            i+=1
        res.append(cur)

        return res



'''
1. lambda函数什么时候使用？
大概就是定义了函数，就使用这么一次，后续不会再用
单独定义这个函数会显得浪费

lambda x:x[0]等价于
def get_start_num(nums):
    return nums[0]
    
2. 怎么看循环停止条件？while i+1<len(intervals)
一开始就是用的i和i+1 --> i+1不能越位（不能超过len(intervals)）

3.怎么看是否要取等？
设数组长度为 L=len(intervals)，下标范围：0,1,...,L-1
要求：i+1 ≤ L-1 --→ i ≤ L-2 --→ i+1 < L

4.为什么最后要在while循环外写res.append(cur)？
while 循环只会在「遇到不重叠区间」时才往 res 里存 cur；
当循环走完（所有 i+1 全部遍历完毕），此时手里的 cur 是最后一组合并完成的区间，
全程没有触发 “不重叠” 分支，所以从来没被 append 到 res 里

5. 判断空数组（加了更完美）： if not intervals:  return []
如果输入 intervals = []，intervals[0] 会直接报错
'''
