from typing import List
from collections import deque
"""
在给定的 m x n 网格 grid 中，每个单元格可以有以下三个值之一：

值 0 代表空单元格；
值 1 代表新鲜橘子；
值 2 代表腐烂的橘子。
每分钟，腐烂的橘子 周围 4 个方向上相邻 的新鲜橘子都会腐烂。

返回 直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回 -1
"""

"""首先要理清这道题的思路-->广度优先遍历
1、从某些起点向外一层一层扩散、蔓延
2、求最短步数 / 最少时间

模板参考前面027二叉数的层序遍历
"""
#1、顺应思路自然而然的解法
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        #参数定义
        queue=deque()
        rows=len(grid)
        columns=len(grid[0])
        directions=[(1,0),(-1,0),(0,1),(0,-1)]
        fresh_num=0
        minutes=0

        #全局搜索找出烂橘子，并添加到队列
        for row in range(rows):
            for column in range(columns):
                if grid[row][column]==2:
                    queue.append((row,column))
                elif grid[row][column]==1:
                    fresh_num+=1

        #看没有烂橘子，没有则返回0
        if len(queue)==0 and fresh_num==0:
            return 0


        #while循环，广度优先遍历
        while queue:
            size=len(queue)
            for _ in range(size): #处理当前层的遍历
                row,column=queue.popleft()

                for dx,dy in directions:
                    next_row=row+dx
                    next_column=column+dy

                    #判断是否越界
                    if next_row<0 or next_column<0 or next_column>=columns or next_row>=rows:
                        continue

                    #判断这个方向相邻的橘子是否是新鲜橘子
                    if grid[next_row][next_column]!=1:
                        continue#不是新鲜橘子
                    grid[next_row][next_column]=2#如果是新鲜橘子，则感染
                    fresh_num-=1
                    queue.append((next_row,next_column))

            minutes+=1

        #如果感染完了，还有新鲜的橘子，返回-1
        if fresh_num>0:
            return -1

        return minutes-1

"""
1、for i in range(n) 与 for _ in range(n)理解
核心区别
_ 和 i 本质都是普通变量，语法上完全一样。
_ 是 Python 约定俗成的写法：这个循环变量我后面完全不用，仅仅只想循环 n 次，我不需要拿到循环的序号

2、当想上下左右进行遍历的时候，前面使用的是递归，这里是while怎么解决的？
使用了directions的数组进行四个方向的遍历

3、continue和pass 的区别
pass空语句、占位符。什么都不干
continue结束本轮循环，直接跳到下一轮，本轮循环剩下代码全部跳过


4、为什么返回的是minutes-1？
因为最后一个被感染的橘子还是会进入队列，因此会多进行一轮for循环
有没有解决方法呢？
-->while queue and fresh_num>0:
用fresh_num本就是为了记录还有多少新鲜橘子，如果没有了，则直接不进入while

四种情况怎么处理的？
（1）一开始有烂橘子，最后全感染了：正常返回
while 循环，同时fresh_num=0

（2）一开始有烂橘子，最后不能全感染：返回 - 1
用fresh_num统计感染前的新鲜橘子，感染一个fresh_num减少1，最后看是否还剩新鲜橘子
if fresh_num>0: return -1

（3）一开始没有烂橘子，只有一堆好橘子：返回 - 1
fresh_num>0,同时queue为空，则while循环不执行

（4）一开始没有烂橘子，也没有好橘子，啥也没有：返回 0
补丁；if len(queue)==0 and fresh_num==0:  return 0
"""

#2、更优雅的写法

class Solution2:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        queue = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    queue.append((i, j))
                elif grid[i][j] == 1:
                    fresh += 1

        minutes = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue and fresh > 0:
            for _ in range(len(queue)):
                x, y = queue.popleft()

                for dx, dy in directions:
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 2
                        fresh -= 1
                        queue.append((nx, ny))

            minutes += 1

        return minutes if fresh == 0 else -1

'''
为什么
'''