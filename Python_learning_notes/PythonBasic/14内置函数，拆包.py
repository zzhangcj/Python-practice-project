# ###1.内置函数
#
# # #1.1查看所有的内置函数
# # import builtins
# # print(dir(builtins))
# # #大写字母开头一般都是内置常量名
# # #小写字母开头一般都是内置函数名，print(),set()....
#
# ##1.2 abs():返回绝对值
# print(abs(-23))#23
# print(abs(23)) #23
#
# # sum():求和
# """
# print(sum(12))
# #TypeError: 'int' object is not iterable
# #整型不是可迭代对象，sum里面要用可迭代对象
#
# print(sum('zcj'))
# #TypeError:
# # unsupported operand type(s) for +: 'int' and 'str'
# #字符串不能相加
# """
#
# print(sum([1,3,4])) #8
# print(sum((1,3,4))) #8
# #列表，元组，集合都可以实现相加
# print(sum({1,3,4.5}))#8.5
#
# #1.3
# # min():求最小值
# # max():求最da值
#
# print(min([1,2,4]))
# print(max({1,2,4}))
#
# print(min(-6,3,key=abs)) #3
# #传入了求绝对值函数，则参数就会先求绝对值再比大小
#
# #1.4 zip():
# # 将可迭代对象作为参数，将对象中对应的元素打包为一个个元组
# li1 = [1,2,3]
# li2 = ['a','b','c']
# print(zip(li1,li2))
# #<zip object at 0x000001844D467A80>
# #这是一个对象，需要把里面的内容取出来
# #第一种方式：通过for循环
# for i in zip(li1,li2):
#     print(i)
# # (1, 'a')
# # (2, 'b')
# # (3, 'c')
# #一一对应形成元组
# print(type(i))#<class 'tuple'>
#
# #如果元素个数不一致，就按照长度最短的返回
#
# #第二种方式：转换为列表打印
# print(list(zip(li1,li2)))
# #[(1, 'a'), (2, 'b'), (3, 'c')]
# #注意：必须是可迭代对象
# """
# print(list(zip(li1,3)))
# #TypeError: 'int' object is not iterable
# """
#
# #1.5 map():能对可迭代对象中每一个元素进行映射，分别去执行
# #map(func,iter1)
# #func为自己定义的函数，iter1为要放入的可迭代对象
# #简单来说就是对象中的每一个元素都会去执行这个函数
# li = [1,2,3,4]
# def funa(x):
#     return x*2
# mp = map(funa,li)#注意：只要写函数名，不用小括号()
# print(mp) #<map object at 0x0000020DD2E4F820>
# #通过for循环取出来
# [print(i) for i in mp]#2 4 6 8
#
# #转换为列表打印[其实也可以使用set(),tuple()]
# print(list(mp))#[2, 4, 6, 8]
#
# funb = lambda x:x*2 #用lambda匿名函数简化
#
# #1.6 reduce()
# #先把对象中的元素取出来，计算一个值保存着，接下来把这个计算值跟第三个元素进行计算
#
# #需要先导包
# from functools import reduce
# #reduce(function,sequence)
# # function---函数：必须是有两个参数的函数
# # sequence---序列：可迭代对象
# li3 = [1,2,3,4]
# def add(x,y):
#     return x+y
# res = reduce(add,li3)
# print(res) #10
#
# fun1 = lambda x,y:x*y
# res1 = reduce(fun1,li3)
# print(res1) #24
#
# """
# 注意只能是两个参数的函数
# fun2 = lambda x,y,z:x*y*z
# res2 = reduce(fun2,li3)
# print(res2)
#
# TypeError: <lambda>() missing 1 required positional argument: 'z'
# """
#

###2.拆包
#含义：对于函数中的多个返回数据，去掉元组，列表或者字典，直接获取里面数据的过程
tua = (1,2,4,5)
print(tua)#(1, 2, 4, 5)
print(tua[1])
#方法一：一般在获取元组的时候使用
a,b,c,d = tua
print('a=',a,'b=',b,'c=',c,'d=',d)
#a= 1 b= 2 c= 4 d= 5

#要求元组内元素个数与接收的变量个数相同，对象内有多少个数据就需要定义多少变量接收
"""
a,b= tua
print(a,b)

#ValueError: too many values to unpack (expected 2)
#报错：值错误，要拆包的值过多
"""
#方法二:一般在函数调用时使用
tua = (1,2,4,5)
a,*b = tua
print(a,b)#1 [2, 4, 5]

def funa(a,b,*args):
    print(a,b)
    print(args,type(args))

funa(1,2,3,4,5,6)
# 1 2
# (3, 4, 5, 6) <class 'tuple'>
arg = (1,2,3,4,5,6,7)#这是一个元组
funa(*arg)
# 1 2  表示元组arg[0],arg[1]两个值分给了a,b.剩下的分给*args
# (3, 4, 5, 6, 7) <class 'tuple'>

tua = (1,2,4,5)
a,*b = tua
c,d,e = b
f,*h = b
print(c,d,e)#2 4 5
print(f,h)#2 [4, 5]
#先把单独的给它取完，其他剩下的全部交给带*的变量










