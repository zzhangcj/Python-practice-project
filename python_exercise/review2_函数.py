##1.参数传递
#写出下面代码的运行结果，并说明核心原理
def func(a, b):
    a = 100
    b.append(200)

x = 10
y = [1, 2, 3]
func(x, y)
print(x, y)
#10 [1,2,3,100]

##2. 默认参数
# 写出两次调用的输出结果，说明 Python 默认参数的经典坑
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item(1)) #[1]
print(add_item(2)) #[1, 2]
'''
1.为什么这里add_item只用传一个参数就行
函数有两个形参：item（必填）、lst（可选，带默认值，默认lst=[]）
调用时只传 1 个参数合法：第二个参数省略，自动使用默认列表；
都没而外传列表-->所有调用共用同一个默认列表对象

2.这个例子想让我知道什么？
定义函数的括号里：def func(x, arr=[]): -→ 可变对象当默认值
❌ 这样写不好，由于共用默认列表，容易产生数据混乱
默认参数的坑就在这里

3.安全规范版本（每次调用新建列表）
def add_item(item, lst=None):
    if lst is None:
        lst = []  # 每次不传lst，这里重新生成全新空列表
    lst.append(item)
    return lst

print(add_item(1))  # [1]
print(add_item(2))  # [2]  符合预期，互不干扰

可变对象不能直接写在函数形参默认位置；统一用 None 占位，函数内部动态创建容器
'''

##3.可变参数 *args 与 关键字参数 **kwargs
def demo(a, b, *args, c=10, **kwargs):
    print(f"a={a}, b={b}, c={c}")
    print("args:", args)
    print("kwargs:", kwargs)

demo(1, 2, 3, 4, d=5, e=6)
'''
a=1, b=2, c=10
args: (3, 4)
kwargs: {'d': 5, 'e': 6}

1。总结
*args 收集所有多余的位置实参，统一打包成元组 tuple
**kwargs 只收集没被函数形参定义过的关键字实参（key=value），打包成字典
注意：是没有被函数形参定义过的
d、e 不在形参列表里 → 进入 kwargs → {'d':5,'e':6}
如果传 a=99：a 是已定义的形参，直接赋值给 a，不会进 kwargs

2.书写顺序：普通位置参数 → *args → 默认参数 → **kwargs
'''
#【编程题】编写一个函数，接收任意多个数字参数，返回所有数字的乘积
def calc_product(*args):
    product=1
    for i in args:
        product *= i
    return product

##4.lambda表达式
f = lambda x, y: x * y + 10
print(f(3, 5)) #25

list1=[(1, 3), (4, 1), (2, 2)]
list1_sorted = sorted(list1,key=lambda x:x[1])
print(list1_sorted)

"""
【简答题】lambda 表达式的特点和适用场景是什么？
特点：匿名函数，只能写一行表达式，自动返回表达式结果，不能包含循环、分支
适用场景：临时简单逻辑、作为sorted/map/filter等函数的 key 参数、无需复用的短小逻辑
"""

##5. 作用域、global、nonlocal
num = 10
def func():
    num = 20
    print("函数内num:", num) #函数内num: 20

func()
print("全局num:", num) #全局num: 10

'''
【代码输出题】写出运行结果，若报错请说明原因
count = 0
def add_count():
    count += 1
    print(count)

add_count()

UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
原因：函数内有count += 1（赋值操作）
Python 规则：函数内只要对变量执行赋值操作，该变量会被判定为局部变量

#解决方案1：global 声明
count = 0
def add_count():
    global count  # 声明使用全局count
    count += 1
    print(count)

add_count()  # 输出：1
'''
