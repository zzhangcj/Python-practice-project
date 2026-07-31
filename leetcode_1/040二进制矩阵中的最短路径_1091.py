from itertools import count
from typing import List
from collections import deque

"""
给你一个 n x n 的二进制矩阵 grid 中，返回矩阵中最短 畅通路径 的长度。如果不存在这样的路径，返回 -1 。

二进制矩阵中的 畅通路径 是一条从 左上角 单元格（即，(0, 0)）到 右下角 单元格（即，(n - 1, n - 1)）的路径
该路径同时满足下述要求：

路径途经的所有单元格的值都是 0 。
路径中所有相邻的单元格应当在 8 个方向之一 上连通（即，相邻两单元之间彼此不同且共享一条边或者一个角）。
畅通路径的长度 是该路径途经的单元格总数。
"""

"""最短路径问题
依旧考虑广度优先遍历
"""
class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        #定义必要的参数
        rows=len(grid)
        columns=len(grid[0])
        queue=deque()
        directions=[(-1,1),(0,1),(1,1),(1,0),(-1,0),(-1,-1),(0,-1),(1,-1)]
        #判断第一个节点是否满足作为起点的条件：即为0
        if grid[0][0]==1:
            return -1
        #初始化队列
        queue.append((0,0))
        grid[0][0]=1 #防止回头
        count=1
        #while+for循环
        while queue:
            size=len(queue)

            for _ in range(size):
                x,y=queue.popleft()
        #判断是否到达终点+边界判断+处理新节点（即防防止回头）
                if x==rows-1 and y==columns-1:
                    return count

                for dx,dy in directions:
                    next_x=x+dx
                    next_y=y+dy

                    if next_y<0 or next_x<0 or next_x>=rows or next_y>=columns:
                        continue

                    if grid[next_x][next_y]!=0:
                        continue
                    grid[next_x][next_y]=1
                    queue.append((next_x,next_y))

            count+=1
        return -1


"""
1、这里的count为什么要赋值为1？
畅通路径长度 = 途经单元格总数
举例：起点(0,0)刚好就是终点（n=1，矩阵只有一格[[0]]）
路径只有自己这一个格子，答案就是1
刚入队的起点(0,0)本身就是路径第一个格子，天然占 1 个长度
对比腐烂橘子：
橘子题目统计消耗的时间（扩散轮次），初始时间 0；
本题统计走过格子数量，起点本身算 1 格，初始 count=1


2、为什么要提前判断到达终点？
队列里的坐标，就是当前正在访问的格子。
如果这个格子正好是终点，当前 count 就是最短路径长度，直接返回

而前一道腐烂橘子使用fresh_num参数
来避免因为最后一个被感染的橘子进入队列造成的多一次循环
这里把终点判断放在这里也是一样的道理，到达终点就不用再走循环，直接返回

3、为什么if grid[next_x][next_y]!=0不能是if grid[next_x][next_y]==1
两者在这道题均可行，但前者更为严谨，确保只有 0 能通行

4、queue.append()里面填入的是元组(),要用小括号包裹

5、总结：
（1）学会使用directions数组来进行方向上的遍历
（2）第二个for循环遍历的是next的节点，要处理的也是next的参数
（3）学会标记访问过的格子，防止回头
"""