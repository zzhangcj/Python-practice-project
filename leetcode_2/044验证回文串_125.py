"""
如果在将所有大写字符转换为小写字符、并移除所有非字母数字字符之后
短语正着读和反着读都一样。则可以认为该短语是一个 回文串

字母和数字都属于字母数字字符。

给你一个字符串 s，如果它是 回文串 ，返回 true ；否则，返回 false 。
"""
#1.暴力一点（不推荐）
class Solution:
    def isPalindrome(self, s: str) -> bool:
        valid=[c.lower() for c in s  if c.isalnum()]
        #return valid == list(reversed(valid))
        return valid==valid[::-1]

'''
1、为什么不是return valid == reversed(valid)
reversed(valid) 返回的是迭代器对象，不是列表
valid == reversed(valid) 是：列表对象 和 迭代器对象做比较，类型不一样，永远返回False，哪怕内容完全一样。
如果要用得用list(reversed(valid))转换为列表
而 valid[::-1] 是生成新列表，是 list，列表和列表对比内容，所以可以正确判断

2、valid=[c.lower() for c in s  if c.isalnum()]
去看review1的#2
'''
#2.双指针（左右）
class Solution2:
    def isPalindrome(self, s: str) -> bool:
        left=0
        right=len(s)-1
        while left<right:
            # 左指针跳过非字母数字
            while left<right and not s[left].isalnum():
                left+=1
            # 右指针跳过非字母数字
            while left<right and not s[right].isalnum():
                right-=1
            # 全部转小写对比
            if s[left].lower()!=s[right].lower():
                return False
            left+=1
            right-=1
        return True
'''
1、我只能想到 while 里面加 if not s [right].isalnum ():，为什么要用 while 里面加两个 while
核心问题：if 只能跳1 次；内层while可以连续跳多个无效字符

2、为什么内层 while 一定要带上 left < right？
防止指针越界。
极端例子：整个字符串全部是符号 ",!!!,, "
如果没有left < right限制：
left 会一直 ++，直接超出字符串下标，访问s[left]触发下标越界报错
'''