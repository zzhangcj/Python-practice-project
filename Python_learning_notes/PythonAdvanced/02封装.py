"""
"""

### 一,封装

# 面向对象的三大特性：封装、继承、多态

##1.封装
#含义：指的时隐藏对象中一些不希望被外部所访问到的属性或者方法
class Person:
    name = 'bingbing'
pe = Person
print(pe.name) #bingbing

Person.name = 'ziyi'
print(pe.name) #ziyi

#2.隐藏属性（私有权限），只允许在类的内部使用，无法通过对象访问
#方法（1）：在属性名或者方法名前面加上两个下划线__
class Person1:
    name = 'James'
    __age = 27 #隐藏属性
p1 = Person1()
print(p1.name)
# print(p1.__age) #报错
#隐藏属性实际上是将名字修改为：_类名__属性名 ,比如 _Person1__age
print(p1._Person1__age) #27
p1._Person1__age = 17
print(p1._Person1__age) #17
#方法（1）不太正规，（了解即可）

#方法（2）：在类的内部使用，比较正规
class Person2:
    name = 'James'
    __age = 27 #隐藏属性
    def introduce(self): #记得加self
        print(f"{Person2.name}的年龄为{Person2.__age}")
        #用 self 访问当前对象的属性，更正规

p2 = Person2()
p2.introduce() #James的年龄为27

'''
正规和不正规区别在于
Python 双下划线 __ 就是“私有成员”，外部对象不建议直接访问
也就是上面所说的只允许在类的内部使用（就是用self访问）
'''




## 3.私有属性/方法
"""
1) xxx:普通属性/方法，无下划线
如果是在类中定义，随便用
类内部能用
对象外部能直接访问、修改
子类能继承
跨文件导入也能正常导入

2) _xxx:约定私有，单下划线开头
私有属性/方法，如果定义在类中，外部可以使用，子类也可继承

只是程序员之间的约定：暗示这是私有，别在外面随便碰
语法上没限制：外部依然能强行访问
子类可以继承
关键点：
另一个py文件用 from 模块 import * 时，带单下划线的不会被导入
大白话:我标了 _ 就是告诉你别乱改，但你硬要改我也拦不住。

3) __xxx:强制私有，双下划线开头
隐藏属性，如果定义在类中
Python 会自动改名 _类名__xxx，外部不能直接访问
不建议、也不应该在类外面直接访问
子类不会直接继承这个私有属性
只能在类内部通过方法间接访问
from xxx import * 也导不进来

这种命名一般是python中的魔法方法或属性，都是特殊含义或者功能的，自己不要轻易定义
"""
class Person3:
    name = '北凉徐凤年'
    __age = 25 #隐藏属性
    _sex = '男' #私有属性

p3 = Person3()
print(p3.name) #正常访问即可
print(p3._sex) #p3.sex会报错，得加下划线
print(p3._Person3__age)#_类名__属性名 才能访问


# 3.1隐藏方法
class Man:
    def __play(self):
        print('玩手机')
    def funa(self):
        print('what can I say!')
        Man.__play(self)
        # 明明是实例方法，非要用类的方式调用
        # 还得手动把 self 传进去，多余又不规范————不推荐
        self.__play()    #推荐使用
        # 用当前对象调用私有方法，不用传参数，Python自动帮你处理
        # 正常在类里面调用自己的方法，统一都是用 self.xxx()
ma = Man()
ma.funa()
# ma._Man__play
# 在类的内部，实例方法互相调用，一律用 self.方法名()

# 3.2私有方法
class Girl:
    def _buy(self): #私有方法，单下划线
        print('整天买买买')
gl = Girl()
gl._buy()















