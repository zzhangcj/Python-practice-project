# ### 1.作用域
# #含义：指的是变量生效的范围，分为全局变量和局部变量
#
# ##1.1全局变量
# #函数外部定义的变量，在整个文件中都是有效的
# a = 12
# def test1():
#     print('a in test1:',a)
# def test2():
#     print('a in test2:',a)
# test1() #a in test1: 12
# test2() #a in test2: 12
#
# b = 11
# def test3():
#     b = 100 #局部变量
#     print('b in test3:',b)
#
# print("调用test3()之前，b=",b)
# #调用test3()之前，b= 11
# test3() #b in test1: 12
# print("调用test3()之后，b=",b)
# #调用test3()之后，b= 11 b的值没有被test里b=100覆盖
# '''
# 因为函数内部要使用变量会先从函数内部找，有的话直接用,没有则会去外面找
# 同时，全局变量和局部变量命名相同，全局变量不会被改变
# '''
#
# ##1.2局部变量
# #函数内部定义的变量，从其定义位置开始到函数定义结束位置有效
# def funa():
#     num = 12
#     print('num=',num)
# funa()#num= 12
# '''
# print(num)
# #NameError: name 'num' is not defined. Did you mean: 'sum'?
# '''
# #局部变量只能在被定义的函数内使用，函数外部不可使用
# #作用：在函数内部，临时保存数据，当函数调用完成之后，就销毁局部变量
#
# ##1.3 global关键字
# #语法格式：global 变量名
#
# #global作用（1）：在函数内部想要修改全局变量的值
# c = 22
# def test4():
#     global c #注意，根据语法格式，不能写成global c = 300,会报错
#     c = 300 #局部变量
#     print('c in test4:',c)
#
# print("调用test4()之前，c=",c)
# #调用test4()之前，c= 22
# test4() #c in test4: 300
# print("调用test4()之后，c=",c)
# #调用test4()之后，c= 300
#
# #global作用（2）：在局部作用域中声明一个全局变量
# def study():
#     global name#将局部变量name声明为全局变量
#     name = "python基础"
#     print(f'我们在学习{name}')
# study() #我们在学习python基础
#
# def work():
#     print(name)
# work() #python基础
#
# #多个变量都要使用global
# def add():
#     global a,b,c
#     a = 1
#     b = 2
#     c = 3
#     return a+b+c
# print(add()) #6
# print(a - b + c) #2
#
# #1.4 关键字nonlocal --了解
# #语法格式：nonlocal 变量名
# # 用来声明外层的局部变量，只能在嵌套函数中使用
# # 在外部函数先声明，内部函数再进行nonlocal声明
#
# a = 10
# def outer():
#     a = 5
#     def inner():
#         nonlocal a
#         a = 20
#         print('inner函数中a=',a)
#     inner()  #inner函数中a= 20
#     print('outer函数中a=',a)
# outer() #outer函数中a= 20
# print('a=',a)#a= 10 没有影响全局变量
# #总结：
# #1.nonlocal只能对上一级函数进行修改，比如这里的a=20影响到了a=5
# #2.但是如果再来一层嵌套，最里层的只能影响中间一层的，最外层不受影响
#
from tkinter.font import names


# ###2.匿名函数
# #2.1基本语法
# # 函数名 = lambda 形参 :返回值(表达式)
# # 调用：结果 = 函数名（实参）
#
# #普通函数
# def add1(a,b):
#     return a + b
# print(add1(1,3)) #4
#
# #匿名函数
# add2 = lambda a,b:a+b #a,b为匿名函数的形参，a+b是返回值的表达式
# #lambda不需要写return来返回值，表达式本身结果就是返回
# print(add2(1,3)) #4
#
# ##2.2lambda的参数形式
# #（1）无参数
# funa = lambda : "一桶水果茶"
# print(funa())#一桶水果茶
#
# #（2）一个参数
# funb = lambda name:name
# print(funb('zcj')) #zcj
#
# #（3）默认参数
# func = lambda name,age = 21:(name,age)
# #有多个参数时，冒号： 之后记得写成元组的形式
# print(func('徐凤年'))#('徐凤年', 21)
# #age使用默认的21
# print(func('徐凤年',23))
# #age传参了，就用上传的23
#
# fune = lambda a,b,c=20:a+b+c#这里返回的是某个值，不用（）
# print(fune(10,30))
# #默认参数必须写在非默认的参数后面，c=20必须在a,b后面
#
# #（4）关键字参数
# fund = lambda **kwargs:kwargs
# print(fund(name = 'zcj',age = 21))
# # {'name': 'zcj', 'age': 21}


##2.3lambda函数结合if判断
"""
特点：lambda只能实现简单的逻辑，如果逻辑复杂且代码量大，不建议使用lambda
会降低代码可读性，后期维护存在困难
"""
a = 5
b = 8
#三目运算：为真结果 if 条件 else 为假结果
print("a<b") if a<b else print("a>=b")
comp = lambda a,b : 'a<b' if a<b else print("a>=b")
#a,b是形参，比较大小
print(comp(4,31))










































