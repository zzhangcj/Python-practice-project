"""
"""

# ### 一.递归函数
# #1.含义：如果一个函数在内部不调用其他函数，而是调用它本身
#
# #2.条件
# #（1）.必须要有明确的结束条件，即递归出口
# #（2）.每进行更深一层的递归，问题规模要比上一次递归减少
# #（3）.相邻的两次重复之间要有紧密联系
#
# #3.案例
# #3.1 普通函数
# def add():
#     sum =0
#     for i in range(1,101):
#         sum += i
#     print(sum)
# add() #5050
#
# #3.2 递归函数
# def add2(n):
#     if n == 1: #如果为1，就返回1 ————明确的结束条件
#         return 1
#     #如果不是1，重复执行累加并返回结果
#     return n + add2(n-1)
# print(add2(100)) #5050
#
# """
# 关于return的理解
#
# 一句话点破你的思维误区
# 你以为：只要里面有一个 return 1，整个函数结束了并返回这个值
# 实际是：每一层 return 都只管自己，每个函数副本的 return，只负责把值传给自己的上一层
# 产生误区的原因是之前学习写的函数，只有一个return，自然就返回这个值作为结果
# 最里层return 1 → 把1返回给中间层拿去做加法并得到中层的结果 → 返回中层结构并用于最外层算出最终结果
# """
#
# ##3.3 递归实现斐波那契数列
# #1，1，2，3，5，8，13....
# #规律为从第三项开始，每一项都等于前两项之和，即n=(n-1)+(n-2)
# def funa(n):
#     if n <= 1:
#         return n
#     return funa(n-1)+funa(n-2)
# print(funa(7)) #13
#
# #3.4 特点
# #优点：简洁，逻辑清晰，解题更有思路
# #缺点：使用递归函数的时候，需要反复调用函数，耗内存，运行效率低
#
#
# ### 二，闭包
# #1.条件
# #（1）函数嵌套(函数里面再定义函数)
# #（2）内层函数使用外层函数的局部变量
# #（3）外层函数的返回值是内层函数的函数名
#
# def outer(): #外层函数
#     n = 10
#     def inner(): #内层函数
#         print(n)
#     return inner
# print(outer())
# #<function outer.<locals>.inner at 0x000001B52D343A60>
# #返回的为内部函数inner的内存地址
#
# #第一种调用写法
# ot = outer() #这个时候return的结果为inner
# ot() #10
# #第二种调用写法
# outer()() #10
#
# def outer2(y):
#     x = 10
#     def inner2():
#         print("计算结果：",x+y)
#     return inner2
# ot2 = outer2(20)
# ot2() #计算结果： 30
#
# def funb():
#     print(123)
# print(funb)
# #<function funb at 0x000002606E483C40>
# #得到的为这个函数的内存地址
#
# #2.id():判断两个变量是否为同一个值引用
# a = 1 #a只不过为一个变量名，存的为1这个值所在的地址，即a里面存了数值1的引用
# #可以理解为指针
# print(a) #1
# print(id(a)) #140717369926568
# a = 2
# print(id(a)) #140717369926600
# print(id(2)) #140717369926600
# #内存地址发生变化，因为值也发生变化
#
# #同理，funa不过也是一个函数名，里面存了这个函数所在位置的引用
#
# """
# 为什么不是return inner2()？
# 不带括号：inner = 函数本身（把整个函数当东西传出去
# 带括号：inner () = 立刻调用执行（马上运行，返回结果）
# 用生活比喻
# inner = 一张菜谱
# inner() = 按照菜谱把菜做出来
# return inner
# = 把菜谱还给你你拿回家，想什么时候做就什么时候做
# return inner()
# = 直接把菜做好端给你
# """

# ##3.每次开启内函数都在使用同一份闭包变量
# def outer(m):
#     print("outer()函数中的值:",m)
#     def inner(n):
#         print("inner()函数中的值:",n)
#         return m+n
#     return inner
# ot = outer(10)
# print(ot(20)) #第一次调用给inner()传值
# # outer()函数中的值: 10
# # inner()函数中的值: 20
# # 30
# #第二次调用内函数
# print(ot(34))
# # inner()函数中的值: 34
# # 44
# #总体来说就是保证m不变的情况下，可以随意操作n的值来得到m+n的不同结果
#
# ## 4.总结
# # 使用闭包的过程中，一旦外函数被调用一次，返回了内函数的引用
# # 虽然每次调用内函数，会开启一个函数，执行后消亡
# # 但是闭包变量实际只有一份，每次开启内函数，都在使用同一份变量


# ### 三.装饰器
# #含义：装饰器本质是就是一个闭包函数，它的好处就是在不修改原有代码的基础上，增加额外的功能
#
# ## 1.作用：在不改变原有代码的情况下，添加新的功能
# #条件（1）不改变原程序或函数的代码
# #条件（2）不改变函数或程序的调用方法
#
# #以下为一装饰器雏形，用于理解装饰器含义（没有满足条件2）
# def test02():
#     print("发送信息给冰冰")
#
# def test(fn): #fn是一个形参，后面用于传入要用的函数名
#     print("开始注册")
#     print("登录")
#     fn() #调用要传入的函数
# test(test02)
# # 开始注册
# # 登录
# # 发送信息给冰冰
# """
# test02 是被添加功能的函数
# test 是给别人加功能的 “装饰工具函数”
#
# 由于原本应该是test02()就能执行，现在得写成test(test02)
# 没有满足条件（2）
# """
#
# ## 2.标准的装饰器
# def send():
#     print("发送消息")
#
# send() #发送消息
#
# #闭包的三个条件（1）（2）（3）
#
# def outer(fn): #外层函数，fn为形参，传入的为被装饰的函数名send
#     def inner(): #（1）函数嵌套(函数里面再定义函数)
#         print("登录吧...") #包含原有的功能同时，添加新 功能
#         fn()     #（2）内层函数使用外层函数的局部变量，这里fn()等同于send()
#     return inner #（3）外层函数的返回值是内层函数的函数名
# print(outer(send))
# #<function outer.<locals>.inner at 0x00000245E1E33A60>
# #是一个内存地址，表示outer(send)这个时候等于inner
# send = outer(send)
# send()
# # 登录吧...
# # 发送消息
# '''
# 这里send()和前面的send()结果已经不一样了，即已经添加了新的功能，但是调用方式没变
# 装饰器的原理就是将原有的函数名重新定义为以原函数为参数的闭包
#
# print(outer(send)) 传入的形参为send，表示要被添加功能的为send
# 如果要给send2，send3修饰呢，这里会显得有些麻烦，这个时候要用"语法糖"
# '''


## 四.语法糖

##1.被装饰的函数没有参数
#格式：@装饰器名称
def outer(fn):
    def inner():
        print("登录...")
        fn()
    return inner

#注意：装饰器之后不要加(),前者为引用，后者为调用函数，返回该函数要返回的值
@outer
def send():
    print("发送消息：笑死我了")
send()
# 登录...
# 发送消息：笑死我了

@outer
def send2():
    print("send a message:hehehe")
send2()
# 登录...
# send a message:hehehe


##2.被装饰的函数存在参数
def outer(fn):
    def inner(name):
        print(f"{name}是inner函数中的参数")
        print("哈哈哈")
        fn(name)
    return inner

# @outer
# def func():
#     print("这是被装饰的函数")
# func()
# '''
# TypeError:
# outer.<locals>.inner() missing 1 required positional argument: 'name'
# 这里报错是因为func()没有参数，但是inner()里面是有参数的，所以func得传参
# '''

@outer
def func(name): #注意这里有没有参数要同步到fn中，保持一致
    print("这是被装饰的函数")
func('bingbing')
# bingbing是inner函数中的参数
# 哈哈哈
# 这是被装饰的函数

##3.被装饰的函数有可变参数*args，**kwargs
def funa(*args,**kwargs):
    print(args)
    print(kwargs)#这里的可变参数不加*,因为这里要print字典kwargs
# funa(name='bingbing') #{'name': 'bingbing'}

def outer(fn):
    def inner(*args,**kwargs):
        print("登录...")
        fn(*args,**kwargs)
    return inner
#函数必须调用才会执行
ot = outer(funa)
print(ot('susu',name='bingbing'))
# 登录...
# ('susu',)
# {'name': 'bingbing'}
"""
* 和 ** 就两个核心作用：打包、解包
定义函数时：*args → 打包
把所有多余的位置参数，打包成一个元组 tuple
def f(*args):
    print(args)
f(1,2,3) # args 被打包成：(1,2,3)

调用函数 / 打印时：*变量 → 解包
把列表、元组，拆成一个个独立的单独参数
lst = [1,2,3]
print(*lst) # 等价于 print(1,2,3)

**kwargs同理，只不过处理的为tuple
"""

## 4.多个装饰器
def deco1(fn):
    def inner():
        return "哈哈哈" + fn() + "呵呵呵"
    return inner

def deco2(fn):
    def inner():
        return "niceeee!" + fn() + "let`s gooooo!"
    return inner

@deco1
@deco2
def test1():
    return "晚上学习python基础"
print(test1())
#哈哈哈niceeee!晚上学习python基础let`s gooooo!呵呵呵
#多个装饰器装饰过程中，离函数最近的装饰器先装饰，然后外面的装饰器再进行装饰，由内到外的装饰过程









