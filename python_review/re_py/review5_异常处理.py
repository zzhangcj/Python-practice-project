"""基础概念"""

# 1、简述try、except、else、finally四个关键字在异常处理结构中的作用与执行时机。
"""
try:
    # 【监控区】放置**可能报错**的代码
except 异常类型 as e:
    # 【故障处理】try内发生对应异常，执行这里
else:
    # 【顺利分支】try代码**没有任何异常**才执行
finally:
    # 【收尾区】无论是否异常、有无return，一定执行；多用于释放资源
"""
# 2、Python 中raise关键字的作用是什么？适用场景有哪些？
"""
主动抛出指定类型的异常，中断程序执行。
适用场景：
业务逻辑不符合规则时（如年龄为负数），主动抛出异常交由上层调用者处理；
自定义异常的抛出；
封装工具类时对外传递错误信息。
"""
# 3、列举至少 5 种 Python 常见的内置异常类，并说明触发场景

# 题目 1：基础异常捕获
try:
    num = int("abc")
    print("转换成功")
except ValueError as e:
    print("值错误", e)
print("程序结束")
#值错误 invalid literal for int() with base 10: 'abc'
#程序结束

# 题目 2：try-except-else 结构
def divide(a, b):
    try:
        res = a / b
    except ZeroDivisionError:
        print("除数不能为0")
    else:
        print("计算结果是", res)
    finally:
        print("执行finally")

divide(10, 2)
divide(10, 0)

# 计算结果是 5.0
# 执行finally
# 除数不能为0
# 执行finally

# 题目 3：经典面试题：return 与 finally 的执行顺序
def test():
    try:
        return 1
    except:
        return 2
    finally:
        return 3

print(test()) #3
'''
原理：finally代码块会在try的 return 语句执行前运行
finally 中的 return 会覆盖 try 分支的返回值，因此最终返回 3
'''

# 题目 4：多异常捕获的顺序问题
try:
    li = [1,2,3]
    print(li[5])
except Exception:
    print("通用异常")
except IndexError:
    print("索引越界")
#通用异常
"""
原理：
异常捕获遵循从上到下依次匹配的规则
Exception是IndexError的父类，会优先匹配成功
后面的IndexError分支永远不会执行
规范写法必须是先写具体异常，最后再写通用的 Exception
"""

# 题目 5：raise 主动抛异常
def check_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    print("年龄合法")

try:
    check_age(-5)
except ValueError as e:
    print("捕获异常：", e)
#捕获异常： 年龄不能为负数

"""编程实操题"""
# 1、自定义异常类AgeIllegalError，继承自Exception；编写函数set_age(age)
# 如果 age 不在 0-120 范围内，抛出该自定义异常；调用函数并捕获处理异常
class AgeIllegalError(Exception):
    pass

def set_age(age):
    if not 0<=age<=120:
        raise AgeIllegalError(f"年龄{age}非法，必须在0-120之间")
    print(f"设置年龄成功：{age}")

try:
    set_age(150)
except AgeIllegalError as e:
    print("捕获到自定义异常：", e)
# 捕获到自定义异常： 年龄150非法，必须在0-120之间

# 2、结合文件操作，编写代码：尝试打开一个不存在的文件not_exist.txt
# 捕获文件不存在的异常并打印提示，无论是否出错，最终都打印 “文件操作结束”。
try:
    with open("not_exist.txt","r",encoding="utf-8") as f:
        content=f.read()
except FileNotFoundError:
    print("错误：文件不存在，无法打开")
finally:
    print("文件操作结束")


"""
总结
1、什么时候用raise，什么时候用try-except？
一句话区分：
✅ try-except：用来接住别人抛出的异常（被动接收）
你调用一段代码，预料它可能报错，你不想程序直接崩溃，准备好应对方案，捕获异常、容错处理
例：打开文件、类型转换、网络请求，预判会出错，加上 try 捕获

✅ raise：主动制造 / 抛出异常（主动发起）
你写函数 / 工具，发现传入的数据不符合业务规则，Python 内置异常无法表达业务错误，主动抛出异常，提醒调用者处理。
例：年龄不能是负数、账号长度不足，主动raise告知调用方参数非法。

2、对于错误类型的理解
（1）except 后面必须是继承自 BaseException 的异常类

（2）一般错误类型后面有解释，可以用 as 来存储这些

（3）知道准确错误类型，就写对应异常名称；不清楚可能抛出什么异常，用 Exception 兜底
优先捕获精确异常，不要一上来就写 except Exception；大范围兜底会掩盖未知 bug，不利于调试。

代码实操题1：
class AgeIllegalError(Exception):
    pass
意思是AgeIllegalError是我自己取的名字，括号里面是Exception，即这个错误类的父类是Exception
"""