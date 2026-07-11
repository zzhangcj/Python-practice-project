class Solution:
    def sum(self,num1: int,num2: int) -> int:
        return num1 + num2

if __name__ == '__main__':
    s = Solution()
    ans=s.sum(12,5)
    assert ans==17,"错了！！！"

# assert表达式
# 如果 条件表达式 == True：代码正常往下走，无任何反应
# 如果 条件表达式 == False：直接抛出 AssertionError，终止程序，并打印后面的提示文字

# int num1,num2
# print(num1+num2)

##问题1： int num1, num2 是静态语言（C/C++/Java） 定义变量的语法，Python 完全不支持这种写法
#Python 定义变量不需要前置声明类型
#正确定义数字变量是：num1 = 1; num2 = 2
#如果要标注类型，只能写成类型注解 num1: int，不能直接 int num1

##问题2：不能用print，LeetCode 不会让你自己定义变量、自己打印输出，平台有固定执行逻辑：
#   后台提前准备好海量测试用例 num1、num2；
#   自动调用 Solution 里的函数，把数字自动传进函数参数；
#   读取函数 return 的返回值对比答案

##问题3：self的知识点回顾
# class 洗衣机 = 图纸，只规定功能，不是真实机器；
# s = 洗衣机()、s1 = 洗衣机() = 造出两台真实洗衣机实例；
# 调用 s.洗衣服() 时，Python 自动把 s 偷偷传给方法第一个参数 self；
# 调用 s1.洗衣服() 时，self 就变成 s1；
# self 的核心作用：让方法知道「当前是哪一台洗衣机在执行操作」