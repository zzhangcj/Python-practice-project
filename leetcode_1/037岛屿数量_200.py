from typing import List
"""
给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。
"""

'''联想上一道题'''
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        count=0
        #找边界
        rows=len(grid)
        columns=len(grid[0])

        def dfs(row,column):
            #边界判断
            if row<0 or row>=rows or column<0 or column>=columns:
                return

            #遇到水(即0)
            if grid[row][column]=="0":
                return

            #遇到陆地(即1)
            grid[row][column]="0" #用水淹掉

            dfs(row-1,column)
            dfs(row+1,column)
            dfs(row,column-1)
            dfs(row,column+1)

        for m in range(rows):
            for n in range(columns):
                if grid[m][n]=="1":
                    count+=1
                    dfs(m,n)
        return count

"""
1、对比前一道题单词搜索
79 单词搜索	临时改成#，递归结束后复原temp，回溯！不能修改原数据
200 岛屿数量	直接原地修改成"0"，不需要复原，永久淹掉陆地

2、为什么岛屿不用回溯复原？
单词搜索：只是试探一条路径，走完要还原棋盘，后面别的起点还要用原始网格。
岛屿数量：统计完一座岛屿，这块陆地已经算过，不需要再重复看，直接永久改成水

3、dfs逻辑
    坐标越界 →返回
    当前是水"0" →返回
    将当前陆地淹为0
    递归上下左右 4 个方向，把相连陆地全部淹掉
"""