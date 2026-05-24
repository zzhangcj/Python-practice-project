# '''
#
# '''
#
# ###1.面向对象和面向过程的区别
# """
# #面向过程：需要实现一个功能的时候，看重的是过程，分析出一个个步骤
# 并把每一个步骤用一个个函数实现，再依次去调用一个个函数即可，每一个步骤必须自己去做
# （就像洗衣服亲自用手洗，需要逐个洗每一件衣物）
#
# #面向对象：需要实现一个功能的时候，看重的是谁帮我做这件事
# （洗衣服可以用机洗，也可以找别人代做）
# """
#
# ##2.类和对象
# #类：对一系列具有相同属性和行为的事物的统称，是抽象的概念，不是真实存在的
# #对象：对类的具体实现，由类创造出来的真实事物，面向对象的核心
# #在开发中，现有类，再有对象
#
# ##2.1 类的三要素
# #（1）类名
# #（2）属性：对象特征的描述，用来说明是什么样子
# #（3）方法：对象具有的功能（行为），用来说明能做什么
#
# #举例：
# #类名：人类
# #属性：身高，体重，年龄
# #方法：走路，说话，学习
#
# #类名：洗衣机
# #属性：大小，长宽
# #方法：洗衣服
#
# ##2.2 定义类
# # class 类名： #类名必须符合标识符规定，同时遵循大驼峰命名法，见名知意
# #    代码块
#
# class Washer:
#     height = 800 #类属性：就是类所拥有的属性
#
# print(Washer.height) #800
#
# #新增类属性：类名.属性名 = 值
# Washer.width = 400
# print(Washer.width) #400
#
# ##2.3 创建对象
# #创建对象的过程，也叫实例化对象
# #实例化对象的基本格式：对象名 = 类名()
# wa = Washer()
# print(wa)
# #<__main__.Washer object at 0x000001E44BAF6900>
# #object 表示对象，这里显示对象在内存中的地址
#
# wa2 = Washer()
# print(wa2)
# #<__main__.Washer object at 0x000001D3D4758910>
# #内存地址不一样，说明是不同的对象，可以实例化多个对象
#
# ##2.4 实例方法
# #注意：由对象调用，至少有一个self参数，执行实例方法的时候，自动调用该方法的对象赋值给self
# class Washer:
#     height = 800
#     def wash(self): #self参数是类中的实例方法必须具备的
#         print("我会洗衣服")
#         print("方法中的self：",self)
# #实例化对象
# wa = Washer()
# print("wa:",wa)
# #wa: <__main__.Washer object at 0x0000024FF7516900>
# #对象调用类中的方法
# wa.wash()
# # 我会洗衣服
# # 方法中的self： <__main__.Washer object at 0x00000260FB306900>
# #wa,self 两个内存地址是一样的，self表示当前调用该方法的对象
# #联想上面注意的部分：自动调用该方法的对象赋值给self，这里wa赋值给了self
#
# wb = Washer()
# print("wb:",wb)
# wb.wash() #这里的self地址和wa的结果不一样
# '''
# 可以理解成，类（洗衣机某型号的图纸）创造了一个对象wa（一台具体的洗衣机），
# 然后在执行方法wash（执行洗衣功能）的时候需要具体的对象（某台洗衣机）去运行，self就相当于调用洗衣机
# '''
# """
# 最直白的一句话总结
# 谁调用方法，self 就是谁！
# wa.wash() → self = wa
# wb.wash() → self = wb
# wc.wash() → self = wc
# self 就是方法内部用来代表 “当前对象” 的固定名字。
#
# 为什么必须要有 self？
# 因为一个类可以创建无数个对象：
# wa = Washer()
# wb = Washer()
# wc = Washer()
# 当调用 wa.wash() 时，Python 必须知道：是哪台洗衣机在洗衣服？→ 靠 self 知道
# """

# ----------------------------------------------------------------------


##2.5 实例属性
#格式：self.属性名
class Person:
    name = 'zcj' #类属性
    def introduce(self):
        print("我是实例方法")
        print(f"{Person.name}的年龄：{self.age}")
pe = Person()
pe.age = 21 #实例属性,在类外面手动加
pe.introduce()
# 我是实例方法
# zcj的年龄：21

#2.5.1 实例属性和类属性的区别
#类属性属于类，是公共的，大家都能访问，实例对象是属于对象的，是私有的
#实例属性只能由对象名访问，不能由类名访问
"""
print(Person.name)
#zcj

print(pe.name)
#zcj

print(Person.age)
#AttributeError: type object 'Person' has no attribute 'age'

pe2 = Person()
print(pe2.age)
#AttributeError: 'Person' object has no attribute 'age'

age是专门给pe的实例属性，其他对象比如pe2依然没有这个属性
pe.age = 21是在类外面手动加的
那如果要在类里面添加，给后续每一个实例化的对象（比如pe2）都要添加age这属性，该如何操作呢
那就是使用构造函数，并传参
"""

#2.6 构造函数__init__()
#作用：init通常用来做属性初始化或者赋值操作
#注意：在类实例化对象的时候，会被自动调用
class Test:
    def __init__(self): #self--实例方法
        print("这里是__init__函数")
te = Test()
# 这里是__init__函数
#创建一个实例对象就完成print，说明被自动调用了

class Human:
    def __init__(self,name,age,height):
        self.name = name
        self.age = age
        self.height = height
        #这里是实例属性，因为已经有了对象名self，不是类属性
    def play(self):
        print(f'{self.name}在打王者荣耀')
    def introduce(self):
        print(f'{self.name}的年龄为{self.age},身高为{self.height}')

h1 = Human('zcj',21,180)
h1.play()
h1.introduce()
# zcj在打王者荣耀
# zcj的年龄为21,身高为180

h2 = Human('cfy',20,170)
h2.play()
h2.introduce()
# cfy在打王者荣耀
# cfy的年龄为20,身高为170


##2.7.析构函数__del__()
#删除对象的时候，解释器会默认调用__del__()方法
class Person:
    def __init__(self):
        print("我是__init__()")
    def __del__(self):
        print("被销毁了")
p = Person()
print("这是最后第二行代码")
print("这是最后一行代码")

# 我是__init__()
# 这是最后第二行代码
# 这是最后一行代码
# 被销毁了
##正常运行时，不会调用__del__(),对象执行结束之后，系统会自动调用__del__

class Person1:
    def __init__(self):
        print("我是__init__()呀呀呀")
    def __del__(self):
        print("被销毁啦啦啦")
p1 = Person1()
del p1
print("这是最后第二行代码呀呀呀")
print("这是最后一行代码哈哈哈")
# 我是__init__()呀呀呀
# 被销毁啦啦啦
# 这是最后第二行代码呀呀呀
# 这是最后一行代码哈哈哈
##dep p1 语句执行的时候，内存会被立即回收，会调用对象本身的__del__()
#__del__()主要是表示该程序或者程序已经全部执行结束




