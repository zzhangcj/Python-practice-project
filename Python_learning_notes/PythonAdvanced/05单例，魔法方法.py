# ###一.单例模式
#
# ##1.理解初始化和空间分配
# class Game:
#
#     game_count = 0   # 类属性
#
#     def __init__(self,name):
#         self.name = name
#         Game.game_count += 1
#
#     # 实例方法
#     def play(self):
#         print(self.name,"正在游戏")
#
#     # 类方法
#     @classmethod
#     def show_count(cls):
#         print("游戏总数：",cls.game_count)
#
# g1 = Game("原神")
# g2 = Game("CSGO")
#
# #理解初始化__init__()
# #g1 = Game("原神")做了两件事
# #1.实例化Game()
# #2.传参，g1给self，"原神"给name
#
# #理解__new__()
# #这里你没有看见new，但是new在背后执行，开辟了一个空间给init使用
#
# ##2.__init__()和__new__()
# #__init__():初始化对象
# class Test1:
#     def __init__(self):
#         print("111这是__init__()")
# t1 = Test1() #这是__init__()
#
# #__new__()：objec基类提供的内置的静态方法
# #作用：1.在内存中为对象分配空间 2.返回对象的引用
# class Test2:
#     def __init__(self):
#         print("222这是__init__()")
#     def __new__(cls, *args, **kwargs):
#         print("222我是__new__()")
#         print(cls)
# t2 = Test2() #我是__new__()
# print('t2:',t2) #t2: None
# # Python默认函数无返回就是None，解释器拿到了None，没拿到真正的对象内存地址
# # 既然没对象，就没必要调用 __init__ 了
# # 最后 t2 = None
#
# #结果没有打印：“__init__()”，被覆盖了
# #类似于：a = 10; a= 20 print(a)的结果为20
#
# #扩展父类功能，用 super().方法名()
# class Test3:
#     def __init__(self):
#         print("333这是__init__()")
#     def __new__(cls, *args, **kwargs):
#         print("333我是__new__()")
#         print(cls)
#         res = super().__new__(cls) #方法重写，res里面保存的是实例对象的引用
#         #由于__new__()为静态方法，形参有cls，实参就得传参
#         #注意：重写__new__()一定要return super().__new__(cls)
#         #否则python解释器得不到分配空间的对象引用，就不会调用__init__
#         return res
# t3 = Test3()
# print('t3:',t3)
#
#
# """
# 总结
# 1.self 是对象
# cls 是类
#
# 2.__new__()是开辟空间创建对象，__init__()初始化对象
# 3.__new__()返回对象引用，__init__()定义实例属性
# 4.__new__()处理的是类，用cls  __init__()处理的是实例，用self
#
# 什么是对象引用：
# res = super().__new__(cls)
# return res
#
# super().__new__(cls) 在内存开辟空间、造空对象
# 返回这个对象的内存地址 = 对象引用，把引用存到 res
# return res 把引用交出去
# 外部 t3 = Test3() 里的 t3 就拿到了这个引用（门牌号）
# 如果你不 return
# __new__ 没把门牌号交出来👉 外面拿到的是None👉 找不到对象，自然不执行__init__
#
# 再区分三个概念
# 类：模板、图纸（Game、Test3）
# 对象/实例：按照图纸造出来的真实房子，在内存里占空间
# 对象引用：房子的门牌号、内存地址，变量 g1、t3 存的就是它
# """
#
# ##3.单例模式
# #含义：可以理解为一个特殊的类，这个类只存在一个对象
# #比如：手机上不能开两个王者荣耀
# #优点：可以节省内存空间，减少了不必要资源浪费
# #缺点：多线程访问的时候容易引发线程安全问题
#
# #3.1方式
# #1）通过@classmethod
# #2）通过装饰器实现
# #3）通过重写__new__()实现 （重点）
# #4）通过导入模块实现
#
# class A:
#     pass
# a1 = A()
# print(a1)#<__main__.A object at 0x00000218D0756CF0>
# a2 = A()
# print(a2)#<__main__.A object at 0x00000218D0938A50>
# #内存地址不同，说明不是一个对象
# #实现单例模式 对象的内存地址都是一样的，只有一个地址
#
# #3.2 通过重写__new_()方法实现单例模式
# #设计流程
# #（1）定义一个类属性，初始值为None，用来记录单例对象的引用
# #（2）重写__new__()方法
# #（3）进行判断，如果类属性是None，把__new__()返回的对象引用保存进去
# #（4）返回类属性中记录的对象
#
# class Singleton:
#     obj = None
#     def __new__(cls, *args, **kwargs):
#         print("这是__new__()方法")
#         #判断类属性是否为空
#         if cls.obj == None:
#             cls.obj = super().__new__(cls)
#         return cls.obj
#     def __init__(self):
#         print("这是__init__()方法哈哈哈哈")
# s1 = Singleton()
# print(s1)
# s2 = Singleton()
# print(s2)
# #运行结果内存地址是一样的
#
# #单例模式：每一次实例化所创建的对象都是同一个，内存地址都一样
# '''
# 理解：
#
# 一、
# obj = None
# 这是类属性，所有实例共享
# 作用：记录我们创建出来的那个唯一对象,一开始是 None，表示还没有对象
#
# 二、核心概念先搞懂
# __new__()：真正创建对象的方法
# 在 __init__ 之前执行，必须返回一个对象
#
# __init__()：给对象初始化赋值的方法
# 对象已经创建好了才会执行它
#
# 三、运行流程
# 第一次：s1 = Singleton ()
# 1.调用 __new__
# 2.obj 是 None → 创建新对象
# 3.把新对象存到 obj
# 4.返回这个对象
# 5.执行 __init__ 初始化
#
# 第二次：s2 = Singleton ()
# 1.调用 __new__
# 2.obj 已经有对象了 → 不创建新的，跳过if，直接return
# 3.直接返回之前那个旧对象
# 4.执行 __init__
#
# 四、总结：重写 __new__，让它永远只创建一个对象，并且永远返回这个对象。
# '''
#
# #3.3 通过导入模块实现单例模式(了解)
# from pytest05_1 import te as te01
# from pytest05_1 import te as te02
#
# print(te01,"te01:",id(te01))
# print(te02,"te02:",id(te02))
# # <pytest05_1.Test object at 0x000001BC9B926900> te01: 1909575543040
# # <pytest05_1.Test object at 0x000001BC9B926900> te02: 1909575543040
#
# #你只需要知道：模块是天然的单例模式
#
# #3.4 单例模式的应用方式
# #1）.回收站对象
# #2）.音乐播放器，一个音乐播放软件负责音乐播放的对象只有一个
# #3）.开发游戏软件 场景管理器
# #4）.数据库配置，数据库连接池的设计


###二、魔法方法&魔法属性
#含义：__xx__()这类形式的方法，比如__init__()，__new__()

#1.__doc__ 魔法属性
# 作用：获取 类 / 函数 / 模块 里面的【文档注释】内容
class Person:
    '''人类的描述信息''' #只能使用多行注释，单行注释无效
    pass
print(Person.__doc__)
#人类的描述信息

def sing():
    """唱歌"""
print(sing.__doc__)

#2.__module__():表示当前操作对象所在模块
#3.__class__():表示当前操作对象所在类
import pytest05_1
b1 = pytest05_1.B()
print(b1)
b1.funa()
print(b1.__module__) #pytest05_1
print(b1.__class__) #<class 'pytest05_1.B'>

#4.__str__():对象的描述信息
#如果类中定义了此方法，那么在打印对象时，默认输出该方法的返回值，也就是打印return中数据
#注意：__str__()必须返回一个字符串
class C:
    def __str__(self):
        return "这里为str的返回值" #必须要有返回值，且为字符串类型.否则报错
c1 = C()
print(c1)

#5.__del__()：析构函数，在程序结束时会调用，或者删除某个对象的时候也会被调用
'''
1.__del__()  对象被销毁时自动执行的收尾方法
程序结束 → 自动调用
手动 del 对象 → 立刻调用
作用：做收尾工作（关闭文件、关闭数据库等）

2.什么时候会自动调用？
有两种情况会触发 __del__()：
程序运行结束，所有对象都要被清理
手动删除对象：del 对象名

3. 它和 __init__() 是一对
__init__()：创建对象时调用（出生）
__del__()：销毁对象时调用（死亡）
'''

#6.__call__():使一个实例对象成为一个可调用对象，就像函数那样被调用
#可调用对象：函数/内置函数和类都是可调用对象，凡是可以把一对()应用到某个对象身上的都可以称之为可调用对象
#callable():判断一个对象是否可以被调用,是则返回True，否则返回False
def func():
    print("好好好")
func() #好好好
print(callable(func)) #True
name = "zcj"
print(callable(name)) #False

#没添加__call__()
class C2:
    def __str__(self):
        return "str返回值"
c2 = C2()
c2()  # 报错！！！
# TypeError: 'C2' object is not callable

#复习一下抛出异常，这里得注释c2()，就是258行代码
try:
    c2()  # 报错！！！
except Exception as e:
    print("出错了", e)

#加了__call__()之后（对象能当函数用）
class C3:
    def __call__(self):
        print("我是__call__方法，对象可以加括号调用啦！")

c3 = C3()
c3()  # ✅ 正常运行！


#调用一个可调用的实例对象，其实就是在调用它的__call__()_方法



