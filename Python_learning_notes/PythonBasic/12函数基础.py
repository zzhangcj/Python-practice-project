### 1.函数
#含义：将独立的代码块组织为一个整体，使其具有特殊功能的代码集，在需要的时候再去调用即可
#作用：提高代码的重用性，使整体代码看上去更加简练

##1.1定义函数
'''
def 函数名():
    函数体
'''

#1.2调用函数：函数名()
def login():
    print('这是登录函数')

login()
login()#调用几次，函数里代码就运行几次，每次调用函数会从头开始运行

#编写一个打招呼的函数并调用它
def say_hello():
    print('hello')
    print('zcj')
    print('21岁')
say_hello()
#注意：函数调用不能放在函数定义前面，会报错

### 2.返回值 return
#作用：函数执行结束后，最后给调用者的一个结果
def buy():
    return '一桶水果茶'
    return 20
buy()
print(buy())#一桶水果茶
#函数中遇到return，表示此函数结束，不继续执行
def buy():
    return '一桶水果茶',20
buy()
print(buy(),type(buy()))#('一桶水果茶', 20) <class 'tuple'>
##总结：
#（1）return返回多个值，以元组的形式返回给调用值
#（2）如果没有返回值，返回结果为None
#（3）如果有一个返回值，正常返回给调用者

## return和print的区别
#（1）return表示子函数结束了，print会一直执行

def funa():
    print(123)
print(funa())
'''
123
None

内部的print会先执行，然后外部的print打印内部print的返回值（即None）
理解比喻：
定义函数不写return，就相当于做题只写”解“和”过程“，不写答案（就是返回值）
于是外部的print，打印的就是None，因为这个函数没返回值（答案）
'''
#（2）return返回计算值，print是打印结果
def add():
    a = 1
    b = 2
    return a+b
print(add())#3

def add():
    a = 1
    b = 2
    print(a+b)
add()#3


### 3.参数
#3.1格式
"""
定义格式：
def 函数名(形参a,形参b):   #形参：定义函数，小括号内的变量
    函数体
    ...（如a=1,b=2）
    
调用格式：
函数名(实参1,实参2)        #实参：调用函数，小括号内的变量
"""
def add(a,b):   #形参a,b
    return a+b
print(add(2,4))#实参2,4 传给a,b

## 3.2必备参数（位置参数：因为只靠位置顺序匹配）
#含义：传递和定义参数的顺序及个数必须一致
'''
def funa(name,name2,name3):
    print(name)
    print(name2)
    print(name3)
funa("zcj")

#TypeError:
# funa() missing 2 required positional arguments: 'name2' and 'name3'
'''
def funa(name,age,gentle):
    print(name)
    print(age)
    print(gentle)
funa("zcj","21","male")
#写了几个参数就必须传几个，不可以多传，也不能少传

## 3.3默认参数
#含义：为参数提供默认值，调用函数时，可以不传该默认参数值
#注意：所有位置参数必须出现在默认参数前，包括函数定义和调用
#格式：def funa(a=2):
def funb(a = 3):
    print(a)
funb()   #3 没有传值会根据默认值执行代码
funb(20) #20 传了值，根据传入值执行代码
'''
def func(a = 3 ,b):
    print(a)
func()

SyntaxError: parameter without a default follows parameter with a default
所有未知参数必须出现在默认参数前
'''

## 3.4可变参数
#含义：传入的值的数量是可以改变的，可以传入多个，也可以不传
#格式：def func(*args)
def func(*args):  #可以把args改成其他参数名，但args更符合规范性
    print(args)
    print(type(args))#<class 'tuple'>  以元组形式接收
func('海绵宝宝','章鱼哥')#('海绵宝宝', '章鱼哥')

## 3.4关键字参数
#格式：def func(**kwargs)
#作用：可以扩展函数的功能
def fund(**kwargs):
    print(kwargs)
fund() #{} ,表示这是个字典，以字典形式接收
fund(name='zcj',age=21)#传值的时候，需要采用 键名=值 的形式
#{'name': 'zcj', 'age': 21}

###4.函数嵌套
##4.1嵌套调用
#含义：在一个函数里面调用另一个函数
def study():
    print('晚上在学习')
def course():
    study()
    print('python基础')
course()

##4.2嵌套定义
#含义：在一个函数中定义另外一个函数
def study1(): #外函数
    print('晚上在学习')
    def course1():  #内函数
        print('python基础')
    course1()
    #这里需要在外函数调用内函数，否则下面指挥运行第一个print
    #注意缩进，定义和缩进是同级的，调用在定义里面则永远调用不到
study1()

'''
def study1():
    print('晚上在学习')
    def course1():
        print('python基础')
        study1() #调用外层函数
    course1()
study1()

陷入死循环，不要在内层函数中调用外层函数
'''









































