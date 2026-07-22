"""
给你一个字符串表达式 s ，请你实现一个基本计算器来计算并返回它的值。
整数除法仅保留整数部分。
注意：不允许使用任何将字符串作为数学表达式计算的内置函数，比如 eval()
"""

'''eval () 接收字符串参数，将字符串解析为 Python 表达式并执行，返回表达式计算结果'''
res="14-3*12/2+4/2"
print(res) #14-3*12/2+4/2
print(eval(res)) #-2.0


class Solution:
    def calculate(self, s: str) -> int:
        s=s.replace(" ","")
        stack=[]
        num=0
        n=len(s)
        pre_sign = "+" #记录前一个运算符，初始化为加号
        for i in range(n):
            char=s[i]
            #如果是数字
            if char.isdigit():
                num=num*10+int(char)

            if not char.isdigit() or i==n-1: #如果是运算符
                if  pre_sign=="+":
                    stack.append(num)
                elif pre_sign=="-":
                    stack.append(-num)
                elif pre_sign=="*":
                    top=stack.pop()
                    plus=top*num
                    stack.append(plus)
                elif pre_sign=="/":
                    top=stack.pop()
                    divide=int(top/num)
                    stack.append(divide)

                pre_sign=char
                num=0

        #栈内所有数字相加得到最终答案
        return sum(stack)


"""计算器，遇到带优先级、括号嵌套的算术表达式求值问题-->要想到栈"""


"""
1.这道题解法运用了栈的思想
当指针在运算符上面的时候，会看前一个符号pre_sign是什么
若是加减，则把前一个运算符搭配前一个数字存入栈
若是乘除，则把取出栈顶元素与前一个数字进行运算

2.关键：这里初始化pre_sign = "+"，是有虚拟头节点的思想
比如：14-3*12/2+4/2 -->第一个减号进行判断pre_sign的时候，让14变成+14是没有影响且能符合思路的

3.为什么要碰到下一个运算符才回头进行判断pre_sign？
确保num是读取完整的，14-3*12/2+4/2 中读取到3*12的1的时候，回头计算则出错
同理，如果读取到2的时候回头计算，如果12这个位置为3位数的时候会出错
所以，当指针到/的时候，能确保12这个位置的数读取完整

4.char.isdigit()
字符串方法：判断字符是否为纯数字
返回 True：字符是 0~9；
返回 False：符号、空格、字母等
'5'.isdigit()  # True
'-'.isdigit()  # False
'*'.isdigit()  # False

5.为什么是if not char.isdigit() or i==n-1: ？
(1)not char.isdigit() → 当前字符是 + - * /运算符
遇到运算符，代表前面连续数字已经读完，立刻根据pre_sign结算这个数字；
(2)i == n-1 → 遍历到字符串最后一个字符
整串末尾没有运算符，最后一段数字永远不会被运算符触发结算，必须手动兜底执行


6.为什么是两个并列的if结构而不是if else？
if char.isdigit():
    拼接数字

if not char.isdigit() or i==n-1:
    结算逻辑

关键：这两段逻辑不互斥，不能 if/else 二选一
如果改成 if ... else ...：一旦执行数字收集分支，就跳过结算分支，末尾数字永远无法结算

7.sum()函数
（1）语法
sum(iterable, start=0)
iterable：可迭代对象（列表、元组、集合等，里面只能放数字）
start（可选）：额外加上的初始值，默认 0
（2）作用
单纯把里面所有数字依次相加，仅此而已，不识别任何运算符、字符串。
"""








