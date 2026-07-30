from typing import List
"""
给定一个 m x n 二维字符网格 board 和一个字符串单词 word
如果 word 存在于网格中，返回 true ；否则，返回 false
单词必须按照字母顺序，通过相邻的单元格内的字母构成，
其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。
同一个单元格内的字母不允许被重复使用

提示：
m == board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board 和 word 仅由大小写英文字母组成
"""

'''
1、先想明白，这道题为什么要想到用回溯算法？
网格种找一条路径，即“如果 word 存在于网格中”
如果要找到这条路径，则需要尽可能的遍历每一种可能-->回溯算法

2、同时为什么提示要说这是一个小网格，要找的word也不长？
因为回溯算法是指数级别的复杂度，如果网格大，路径长则非常容易超时

3、注意，其实这道题也算一种图论搜索
'''
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows=len(board)
        columns=len(board[0])
        word_len=len(word)

        def backtracking(row,column,i):
            #回溯的套路1：边界条件
            #（1）处理越界
            if not (0<=row<rows and 0<=column<columns):
                return False
            #（2）避免重复走过
            if board[row][column]=="#":
                return False
            #（3）不是要找的
            if board[row][column]!=word[i]:
                return False
            #（4）防止i越界
            if i==word_len-1:
                return True

            # 回溯的套路2：当前位置处理
            temp=board[row][column]
            board[row][column]="#"

            #回溯的套路3：递归且回溯
            #递归
            found=(
                    backtracking(row, column + 1, i + 1) or
                    backtracking(row, column - 1, i + 1) or
                    backtracking(row + 1, column, i + 1) or
                    backtracking(row - 1, column, i + 1)
            )

            #回溯
            board[row][column]=temp

            return found

        #调用
        for m in range(rows):
            for n in range(columns):
                #找开头并开始查找路径
                if board[m][n]==word[0] and backtracking(m,n,0):
                    return True
        return False


"""
1、为什么要rows，columns这两个参数，以及为什么是这样计算得到的
这两参数是为了进行边界判断以及，遍历board

2.为什么if i==word_len-1要在最后面？
前面 3 道if全部放行，代表word[i]已经成功匹配；
此时如果 i 正好是单词最后下标，也满足前3个if，满足条件，直接就地返回 True，不再发起下一层递

3.if not (0<=row<rows and 0<=column<columns)
能不能去掉小括号写成if not 0<=row<rows and 0<=column<columns
不能，因为这样not只管0<=row<rows


4.知识补充：from collection import Counter
(1)Counter函数的用法
Counter 是字典 dict 的子类，专门用来统计元素出现次数（计数）

#方式1：直接传入可迭代对象(字符串、列表)，直接统计
c1 = Counter("aabbc")
print(c1)   # Counter({'a':2,'b':2,'c':1})

c2 = Counter(["A","B","C","A"])
print(c2)   # Counter({'A':2,'B':1,'C':1})

#方式2：创建空计数器，后续update填充数据
c3 = Counter()
c3.update(["A","B"])
print(c3) # Counter({'A':1,'B':1})
c3.update(["A"])
print(c3) # Counter({'A':2,'B':1})

update(可迭代对象)不是覆盖！
累加计数，把传入序列里面所有元素统计数量叠加到原来 Counter 上

#方式3取值：和字典一样，c['key']
print(c1['a']) #2

#❗超级友好特性：如果key不存在，返回0，不会报KeyError
print(c1['z']) #0，普通dict访问不存在key直接报错
    
(2)什么时候想起使用Counter？
只要题目需要统计元素出现频率、统计个数，优先 Counter
"""
#进阶：剪枝
from collections import Counter
class Solution2:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows=len(board)
        columns=len(board[0])
        word_len=len(word)

        #统计棋盘全部字符频率
        board_counts=Counter()
        for row in board:
            board_counts.update(row)

        word_counts=Counter(word)
        # 剪枝1：频率核对（校验）
        # 如果单词里某个字母的需求量，超过了迷宫的存货量，直接提前剪枝
        for char,count in word_counts.items():
            if board_counts[char]<count:
                return False
        # 剪枝2：首位反转优化
        # 如果某个单词首字母往后重复很多，在迷宫里泛滥（导致起点太多，会出现很多不必要的遍历）
        # 而尾字母稀缺，就把单词反转，减少起点数量
        if board_counts[word[0]]>board_counts[word[-1]]:
            word=word[::-1]

        def backtracking(row,column,i):
            #回溯的套路1：边界条件
            #（1）处理越界
            if not (0<=row<rows and 0<=column<columns):
                return False
            #（2）避免重复走过
            if board[row][column]=="#":
                return False
            #（3）不是要找的
            if board[row][column]!=word[i]:
                return False
            #（4）防止i越界
            if i==word_len-1:
                return True

            # 回溯的套路2：当前位置处理
            temp=board[row][column]
            board[row][column]="#"

            #回溯的套路3：递归且回溯
            #递归
            found=(
                    backtracking(row, column + 1, i + 1) or
                    backtracking(row, column - 1, i + 1) or
                    backtracking(row + 1, column, i + 1) or
                    backtracking(row - 1, column, i + 1)
            )

            #回溯
            board[row][column]=temp

            return found

        #调用
        for m in range(rows):
            for n in range(columns):
                #找开头并开始查找路径
                if board[m][n]==word[0] and backtracking(m,n,0):
                    return True
        return False