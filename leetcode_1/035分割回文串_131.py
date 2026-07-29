"""
给你一个字符串 s，请你将 s 分割成一些 子串，
使每个子串都是 回文串 。返回 s 所有可能的分割方案

示例 1：

输入：s = "aab"
输出：[["a","a","b"],["aa","b"]]

示例 2：
输入：s = "a"
输出：[["a"]]

提示：
1 <= s.length <= 16
s 仅由小写英文字母组成
"""
from typing import List

'''返回 s 所有可能的分割方案-->看到”所有方案“-->想到回溯算法'''

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        res=[]
        path=[]
        n=len(s)

        def is_palindrome(left,right):
            while left <right:
                if s[left]!=s[right]:
                    return False
                left+=1
                right-=1
            return True

        def backtrack(start_index):
            if start_index>=n:
                res.append(path.copy())
                return

            for i in range(start_index,n):
                if is_palindrome(start_index,i):
                    path.append(s[start_index:i+1])
                    backtrack(i+1)
                    path.pop()

        backtrack(0)
        return res

"""
和前面回溯算法问题的新知识点：
1. 切割问题：
之前题目：选数组里的元素，path.append(nums[i])，拿单个元素
本题：切割字符串，截取一段子串，path.append(s[start_index:i+1])
子集：从 start_index 开始选元素
分割回文：从 start_index 开始选一段区间子串

start_index：上一刀切完的下一个起始位置。
i：这一刀切到 i 位置，子串就是 [start_index, i]。
下一层递归就从 i+1 继续切

2.终止条件 if start_index>=n
start_index >= n 代表整根字符串全部切割完毕，没有剩余字符
此时 path 就是一套完整分割方案，收集结果。

3.is_palindrome 函数，我也想到了，但 if 条件我最先想到的是 ==，而不是!=
怎么才能判断当前情况改用哪个？

判断 “是不是 XX” 的布尔函数，优先找反例（!=）。
找到反例直接返回 False；全部走完没问题再返回 True

什么时候，要用 ==（找符合条件）
场景：只要存在任意一个满足条件就成功；或者做统计、收集


4.is_palindrome 函数简写
def is_palindrome(left,right):
    sub = s[left:right+1]
    return sub == sub[::-1]


"""