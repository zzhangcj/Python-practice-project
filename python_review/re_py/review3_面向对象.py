# 1. 基础概念：class、init、self
# 【代码输出题】写出运行结果
from platform import python_version


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = Student("张三", 20)
s2 = Student("李四", 22)
print(s1.name, s2.age)
#张三 22

# 【简答题】__init__方法的作用是什么？它是类的构造函数吗？
'''
__init__函数是初始化函数 -->给实例对象初始化属性
__new__函数才是构造函数 -->开辟空间，创建实例对象
'''

# 【简答题】类实例方法中的self关键字是什么？必须命名为self吗？
'''
self 代表当前正在被实例化的对象本身，实例方法的第一个参数默认就是实例对象本身
不必须叫 self，只是 Python 社区的约定俗成，改成其他名字语法也能运行，但不推荐
'''

# 2. 封装
# 【代码输出题】写出运行结果，若报错请说明原因
class Person:
    def __init__(self, name, id_card):
        self.name = name
        self.__id_card = id_card

p = Person("王五", "123456")
print(p.name) #王五
'''
print(p.__id_card)
#AttributeError: 'Person' object has no attribute '__id_card'
双下划线开头的__id_card是私有属性，外部无法直接通过属性名访问
'''

'''
【编程题】完善Person类：私有属性__age，提供get_age()读取年龄、set_age()设置年龄
设置时必须校验年龄在 0-120 之间，否则提示非法。
'''
class Person:
    def __init__(self, age):
        self.__age = age

    def get_age(self):
        return self.__age

    def set_age(self, new_age):
        if 0 <= new_age <= 120:
            self.__age = new_age
        else:
            print("年龄非法，必须在0-120之间")
p=Person(40)
print(p.get_age()) #40
p.set_age(50)
print(p.get_age()) #50

# 3. 继承、super ()
# 【代码输出题】写出运行结果--->继承
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        print(f"{self.name}发出叫声")

class Dog(Animal): #继承父类Animal的属性和方法
    def speak(self):
        print(f"{self.name}汪汪叫")

dog = Dog("旺财")
dog.speak() #旺财汪汪叫
#子类重写了父类的speak方法，实例调用时优先执行子类的方法


# 【代码输出题】写出运行结果--->super()
class Base:
    def __init__(self):
        print("Base初始化")

class A(Base):
    def __init__(self):
        print("A初始化前")
        super().__init__()
        print("A初始化后")

a = A()
# A初始化前
# Base初始化
# A初始化后
'''
【简答题】super()函数的作用是什么？和直接用「父类名。方法名」调用相比有什么区别？

如果要对父类的方法进行扩展：继承父类的方法，子类也可以增加自己的功能，怎么办？

方法(1)：父类名.方法名(self)
Person3.property(self)

方法(2)：super().方法名()---推荐使用
super在python里面是一个特殊的类，super()表示使用super类创建出来的对象，可以调用父类中的方法

方法（1）的缺陷
缺点 1：类名写死了，改类名全要改
比如子类对某个方法重写了，但以后这个方法要在父类里面被修改 -->这个时候就还得改子类的东西
以后如果要把父类 Person3 改名叫 PersonNew
代码里所有 Person3.property(self) 全都要手动改，漏一个就报错
而super()自动适配

缺点 2：多继承的时候直接废了
多继承，一个子类有好几个父类，根本不知道该写哪个父类名
super() 能自动帮你按顺序找。

当子类重写父类方法，需要复用父类原有逻辑并扩展自身功能时，使用super()获取父类代理对象调用父类同名方法

'''

# 【代码输出题】写出运行结果--->多继承
class A:
    def test(self):
        print("A.test")
class B:
    def test(self):
        print("B.test")
class C(A, B):
    pass

c = C()
c.test() #A.test
'''
Python 多继承遵循 MRO 顺序，C(A, B)的方法查找顺序是 C → A → B → object
因此优先执行 A 类的 test 方法
'''

# 4. 多态
# 【代码输出题】写出运行结果
class Cat:
    def speak(self):
        print("喵喵")
class Duck:
    def speak(self):
        print("嘎嘎")

def make_sound(animal):
    animal.speak()

make_sound(Cat()) #喵喵
make_sound(Duck()) #嘎嘎

'''
【简答题】Python 中的多态是什么？它的实现依赖什么特性？
定义：同一个函数 / 接口，传入不同的对象，会执行不同的逻辑，产生不同的结果
'''

"""
5. 类的设计思考
【简答题】为什么要使用类（面向对象编程）？
把一组数据和操作这些数据的方法封装成类封装成类，只需要暴露必要的接口
通过实例化对象，调用接口来实现功能
这样的代码能多次使用，支持继承，子类可以直接复用父类已写好的代码，方便修改和维护

【简答题】什么场景下不适合使用类？
(1)逻辑简单、只有少量独立函数的脚本，用函数式编程更简洁
(2)一次性、无复用需求的临时代码
(3)仅存储数据、无操作方法的场景，用字典、元组、dataclass 更轻量
(4)纯函数式计算、无状态维护需求的场景
"""