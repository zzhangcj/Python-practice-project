# ### 二.继承
#
# #含义：让类和类之间转变为父子关系，子类默认继承父类的属性和方法
# #语法：class 类名(父类名)：
# #         代码块
#
#
#
# ##1.单继承
# class Person1:
#     def eat(self):
#         print("I can eat!")
#     def sing(self):
#         print('I am good at singing!')
#
# class Girl(Person1): #Person的子类
#     pass #占位符，代码里面的类下面不写任何东西的时候使用
#          #作用是自动跳过，不产生报错
# class Boy(Person1):
#     None #补充：也可以写None
#
# # pass ✅ 正确、无警告、专门用于占位
# # None ⚠️ 表示空，无用代码、编辑器会黄色警告
#
# girl = Girl()
# girl.eat() #I can eat!
# girl.sing() #I am good at singing!
# boy = Boy()
# boy.eat() #I can eat!
# boy.sing() #I am good at singing!
# '''
# 总结：子类可以继承父类的属性和方法，就算子类没有，也可以使用父类的
# '''
#
#
# ##2.多重继承（继承的传递）
# #A/B/C  C(子类)继承于B(父类)，B(子类)继承C(父类)，C类具有A/B的属性和方法
#
# class Father:
#     def eat(self):
#         print('吃饭')
#     def sleep(self):
#         print('睡觉')
#
# class Son(Father):
#     pass
# son = Son()
#
# class Grandson(Son):
#     pass
# gson = Grandson()
# gson.eat()  #吃饭
# gson.sleep()#睡觉
#
# #继承的传递性就是子类拥有父类以及父类的父类的属性和方法
#
# ##3.重写：子类中定义与父类相同的名称的方法
# #3.1 覆盖子类的方法：
# class Person2:
#     def property(self):
#         print("One million needs to be inherited")
# class Man(Person2):
#     def property(self):
#         print("I can earn 10 million by myself")
#
# man = Man()
# man.property()
# #I can earn 10 million by myself
#
# #3.2 对父类的方法进行扩展：继承父类的方法，子类也可以增加自己的功能
# #方法(1)：父类名.方法名(self)
# #Person3.property(self)
#
# #方法(2)：super().方法名()---推荐使用
# #super在python里面是一个特殊的类，super()表示使用super类创建出来的对象，可以调用父类中的方法
#
# #方法(3).super(子类名,self).方法名()
# #完整、啰嗦版的super(), Python2 时代的老式写法，现在 Python3 基本不用了
# """
# super() 就是自动帮你找到 父类的一个代理对象，不用你手动写死父类名字，直接调用父类的方法。
# 可以类比# 不推荐Man.__play(self)  # 推荐self.__play()
#
# 方法1的缺陷
# 缺点 1：类名写死了，改类名全要改
# 以后如果要把父类 Person3 改名叫 PersonNew
# 代码里所有 Person3.property(self) 全都要手动改，漏一个就报错
# 而super()自动适配
# 缺点 2：多继承的时候直接废了
# 多继承，一个子类有好几个父类，根本不知道该写哪个父类名
# super() 能自动帮你按顺序找。
# """
#
# class Person3:
#     def property(self):
#         print("One million needs to be inherited")
#     def sleep(self):
#         print("I like sleeping")
# class Man1(Person3):
#     def property(self):
#         Person3.property(self)
#         super().property()
#         super().sleep()
#         print("I can earn 10 million by myself")
#
# m1 = Man1()
# m1.property()
# # One million needs to be inherited---Person3.property(self)
# # One million needs to be inherited---super().property()
# # I like sleeping
# # I can earn 10 million by myself



##4.新式类写法
# 分类：经典类，派生类，新式类
class A1: #经典类：不由任意内置类型派生出的类
    pass
class Animal:
    def walk(self):
        print("I can walk")
class Dog(Animal): #派生类:只要一个类继承了别的类，它就是派生类,就是子类
    def bite(self):
        print("Dogs can bite people")


class A():
    pass
#Python3 中，你写的所有类，不管写不写继承，默认都是新式类
class A(object):
    pass
'''
新式类：继承了object类或者该类的子类都是新式类
object--对象，python中所有的对象提供的基类（顶级父类）,也就是所有的类都继承object类
提供了一些内置的属性和方法，可以使用dir()查看
print(dir(object))

python3中如果一个类没有继承任何类，则默认继承object类，因此python3都是新式类
'''

#以class Dog(Animal)为例，Dog既是派生类(Animal的子类)，也是新式类

##5.多继承
#子类可以拥有多个父类，并且具有所有父类的属性和方法
class Father(object):
    def property(self):
        print("One million needs to be inherited")
class Mother(object):
    def appearance(self):
        print("Unparalleled beauty needs to be inherited")
    def property(self):
        print("You can inherit ten thousand ")

class Son(Father,Mother): #Father在前面，优先Father里的property
    pass
son = Son()
son.property()
son.appearance()
# One million needs to be inherited
# Unparalleled beauty needs to be inherited

#5.1 不同的父类存在同名的方法
#实际开发的时候，需要尽量避免这样的情况
class Daughter(Mother,Father): #Mother在前面，优先Mother里的property
    pass
daughter = Daughter()
daughter.property()
daughter.appearance()
# You can inherit ten thousand
# Unparalleled beauty needs to be inherited
#有多个父类的属性或者方法，如果多个父类具有同名方法的时候，调用就近原则
#就是看括号内哪一个离得最近（谁在更左边），优先调用哪一个类的方法

#5.2 方法的搜索顺序（了解）
#（1）python中内置属性__mro__可以查看方法搜索顺序
print(Son.__mro__)
print(Daughter.__mro__)

#（2）搜索方法时，会按照__mro__的输出结果，从左往右的顺序查找
#（3）如果在当前类中找到了方法，就直接执行，不再搜索
#比如：在Son里面，def property(self),则直接调用Son的property，Father，Mother里则不再用
#这里看上面__mro__的结果，Son在最前面

#5.3 多继承的弊端
#（1）容易引发冲突
#（2）会导致代码设计的复杂度增加




















