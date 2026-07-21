###一.多态
#含义：指同一种行为具有不同的表现形式
#前提：继承，重写

print(10+10) #算数运算符：可以实现整型之间的的相加操作
print('10'+'10') #字符串拼接符：实现字符串拼接

class Animal():
    def shout(self):
        print("animal can shout")
class Cat(Animal):
    def shout(self):
        print("miao miao miao")
class Dog(Animal):
    def shout(self):
        print("wang wang wang")
cat = Cat()
cat.shout() #miao miao miao
dog = Dog()
dog.shout() #wang wang wang
'''
可以看到shout输出了不同的内容，这是重写（override）
'''

# 多态性：一种调用方式，不同的执行结果
# 多态性的核心：同一个方法名，不同对象调用，自动表现不同行为
def make_sound(animal): #这里的animal为形参，可以为其他名字
    animal.shout()  # 关键：这里不知道 animal 具体是猫还是狗

make_sound(Animal()) # animal can shout
make_sound(Cat())  # miao miao miao
make_sound(Dog())  # wang wang wang
'''
自己单独调用：只是重写
统一用父类接收、一个函数适配所有子类：这才是多态
'''


"""
补充：
1.Python 里 class Person和 class Person()完全一模一样，没任何区别
Python2年代，必须写继承父类 object
Python3年代，所有类默认自动继承 object

2. 什么时候括号里必须写东西？
只有你要手动继承别的类时，才需要写括号：
主动继承 Animal
class Cat(Animal):
    pass
"""
###二.静态方法
#使用@staticmethod来进行修饰，静态方法没有self，cls参数的限制
#静态方法本质上就是“放在类命名空间里的普通函数”，所以可以被转换成函数使用
class Person(object):
    # 静态方法：通用功能，和具体某个人无关
    @staticmethod
    def study():
        print("All the people can study")

    # 静态方法：只依赖传入参数，不依赖对象自身数据
    @staticmethod
    def run(name):
        print(f"{name} can run fastly")

    # 普通实例方法：必须用 self，属于具体某一个人自己的行为
    def speak(self,name):
        print(f"{name} can speak English")

#静态方法既可以使用对象访问，也可以使用类访问
# 1. 类名直接调用静态方法
Person.study()
Person.run("zmjjkk")
# All the people can study
# zmjjkk can run fastly

# 2. 对象也能调用静态方法（但不推荐，只是语法允许）
pe = Person()
pe.study()
pe.run("zcj")
# All the people can study
# zcj can run fastly

# 实例方法调用演示
# 必须先创建带自己属性的对象
p1 = Person()
# 实例方法只能用对象调用，自动传 self
p1.speak('zcj') #zcj can speak English

#错误示例
'''
def speak(self,name): #有self
    print(f"{name} can speak English")
Person.speak('zcj')
#TypeError: Person.speak() missing 1 required positional argument: 'name'
# Person.speak () 缺少一个必须的位置参数：name
# 你以为：传了 zcj → 给 name
# 但Python实际理解：zcj → 传给了第一个参数self，第二个参数name完全没传！
# 所以报错：缺少 name 参数！

def speak(name): #缺少self
    print(f"{name} can speak English")
pe.speak('zcj')
结果：
TypeError: Person.speak() takes 1 positional argument but 2 were given
多传了一个参数
# 原因：
# 普通实例方法中，第一个参数必须是 self
# 因为你用对象调用方法时：运行pe.speak('zcj')
# Python 会自动把 pe 这个对象当作第一个参数传进去！也就是说：
# pe.speak('zcj')=== 等于 ===> Person.speak(pe, 'zcj')

所以你的方法必须写成：
def speak(self, name)，或者使用静态方法@staticmethod，让方法不受self限制

总结：@staticmethod可以取消不必要的参数传递
'''

###三.类方法
#使用装饰器@classmethod来标识的为类方法，第一个参数必须是类对象，一般是以cls为作为第一个参数
#class 类名：
#    @classmethod
#     def 方法名(cls,形参):
#         方法体
#类方法内部可以访问类属性，或者调用其他类方法
class Human():
    name = 'bingbing'
    @classmethod
    def sleep(cls):
        print(cls) #cls代表类对象本身，类本质上是一个对象
        print("people can sleep")
        print(cls.name)

Human.sleep()
# <class '__main__.Human'>      print(cls)的结果
# people can sleep
# bingbing
#当方法中需要使用到类对象（如访问私有类属性等），定义类方法
#类方法一般配合类属性使用

print(Human) #<class '__main__.Human'>
#Human是类本身,它是一个模板、图纸,打印出来就是：这是一个叫 Human 的类

print(Human()) #<__main__.Human object at 0x000002635A726CF0>
#Human()是把类实例化 = 就是按图纸造出来的一个对象
#后面那串 0x... 是内存地址，表示这个对象在电脑内存哪放着

print(type(Human)) #<class 'type'>
#理解部分看下面
'''
#1.先理解“类对象”
class Human():
   .....
   
print(type(Human)) #<class 'type'>   
很多人以为：Human 是“类定义”，其实Human本身也是一个对象
类本身也是 type 类创建出来的对象

#2.理解这里三种打印结果的含义（看上面注释），以及__main__是什么
__main__ 表示：这个类是在「当前运行的这个 py 文件」里定义的

#3.理解cls，先看上面Human.sleep()的结果里面
<class '__main__.Human'>      print(cls)的结果
与print(Human) #<class '__main__.Human'>相同
说明：cls代表类对象本身（即模板，图纸），类本质上是一个对象
cls.name 就是访问类里面的类属性
'''


"""
总结

1.比喻：
类（class）：游戏角色模板
对象（instance）：真正创建出来的角色
类属性：所有角色共同规则
实例属性：每个角色自己的血量、名字
实例方法：某个角色自己的行为
类方法：修改整个游戏规则的方法/模板
静态方法：放在游戏类里的工具函数/帮助函数

2. 静态方法（@staticmethod）
和对象无关，和类状态也无关，只是写在类里面方便管理和后续处理
可以理解为“分类管理工具”

"""


class Game:

    game_count = 0   # 类属性

    def __init__(self,name):
        self.name = name
        Game.game_count += 1

    # 实例方法
    def play(self):
        print(self.name,"正在游戏")

    # 类方法
    @classmethod
    def show_count(cls):
        print("游戏总数：",cls.game_count)

    # 静态方法
    @staticmethod
    def tips():
        print("适度游戏益脑")

g1 = Game("原神")
g2 = Game("CSGO")

#理解__init__() -->初始化函数
#g1 = Game("原神")做了两件事
#1.实例化Game()
#2.传参，g1给self，"原神"给name

#理解__new__() -->构造函数
#这里你没有看见new，但是new在背后执行，开辟了一个空间给init使用


