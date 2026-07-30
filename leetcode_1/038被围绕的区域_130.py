from typing import List
"""
给你一个 m x n 的矩阵 board ，由若干字符 'X' 和 'O' 组成，捕获 所有 被围绕的区域：

连接：一个单元格与水平或垂直方向上相邻的单元格连接。
区域：连接所有 'O' 的单元格来形成一个区域。
围绕：如果一个区域中的所有 'O' 单元格都不在棋盘的边缘，则该区域被包围。这样的区域 完全 被 'X' 单元格包围。
通过 原地 将输入矩阵中的所有 'O' 替换为 'X' 来 捕获被围绕的区域。你不需要返回任何值。

"""

"""
关键：边界反向搜索
如果直接处理内部都为O的区域-->十分复杂
反向思维：因为与边界有接触的O所在的块不会被处理
-->找到这个边界的连通块，标记临时符号#，则剩下的O所在的块就是需要被改成X的
-->重新遍历整个board，如果找到O则改成X，如果找到#，则还原为O
"""
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows=len(board)
        columns=len(board[0])

        def dfs(row,column):
            if row>=rows or row<0 or column>=columns or column<0:
                return

            #碰到X 或 #
            # if board[row][column]=="X":
            #     return
            # if board[row][column]=="#":
            #     return
            if board[row][column]!="O": #等价上面两种情况
                return

            #处理O
            board[row][column]="#"

            dfs(row-1,column)
            dfs(row+1,column)
            dfs(row,column-1)
            dfs(row,column+1)


        #两个for循环处理边界，把边界的O替换为#
        for row in range(rows):
            if board[row][0]=="O":
                dfs(row,0)
            if board[row][columns-1]=="O":
                dfs(row,columns-1)
        for column in range(columns):
            if board[0][column]=="O":
                dfs(0,column)
            if board[rows-1][column]=="O":
                dfs(rows-1,column)

        #遍历board,O替换为X,X替换为O
        for m in range(rows):
            for n in range(columns):
                if board[m][n]=="O":
                    board[m][n]="X"
                elif board[m][n]=="#": #注意必须是elif
                    board[m][n]="O"


"""
为什么最后的这里必须是elif？

防止同一轮循环内，修改完本单元格之后，又被后续 if 再次修改
if ... elif：互斥，只会走其中一个分支，执行完直接跳过后面条件，确保同一个格子最多执行一次修改

#危险示范
if board[m][n]=="#":
    board[m][n]="O"
if board[m][n]=="O":
    board[m][n]="X"
单元格原始值"#"
第一个 if 命中："#" → 修改成"O"
此时变量已经变成 O！第二个 if 又判断，条件再次满足
又执行一遍，把刚刚改好的"O"又覆盖成"X"，出错
"""