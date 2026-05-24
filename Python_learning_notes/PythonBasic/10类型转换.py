### 1.类型转换
#1.1.1 int():转换为一个整数，只能转换为由纯数字组成的字符串
a = 1.2
print(type(a))#<class 'float'>
b = int(a)
print(b,type(b)) #1 <class 'int'>

#1.1.2 浮点型强转整型会去掉小数点以及后面的数值，只保留整数部分
#str -> int
a = '124'
print(int(a),type(int(a)))#124 <class 'int'>
#print(int(’zcj‘)) 会报错
#如果字符串中有数字和正负号(+/-)以外的字符会报错
#(+/-)写在前面表示正负，不可以写在后面
'''
print(int('10-'))
ValueError: invalid literal for int() with base 10: '10-'
'''

#用户从控制台输入，判断年龄
age = input("请输入你的年龄：")
print(type(age)) #<class 'str'>
#pirnt()函数在控制台收到的输入，是字符串类型，要使用得强制转换

age = int(input("请输入你的年龄："))
if age >=18:
    print("成年了")


##1.2 float():转换为一个小数
print(float(11))#11.0  整型转换为浮点型，会自动添加一位小数
print(float(-11))#-11.0
print(float('-213.23'))#-213.23
'''
print(float('10-'))#报错
如果字符串中有正负号，数字，小数点以外的字符，则不支持转换
'''

##1.3 str():转换为字符串类型，任何类型都可以转换为字符串类型
n = 100
print(type(n))#<class 'int'>
n2 = str(n)
print(n2,type(n2))#100 <class 'str'>

st = str(-23.20)
print(st,type(st)) #-23.2 <class 'str'>
#float转换为str,会去除末尾为0的小数部分
li = [1,2,3]
st = str(li)
print(st,type(st))#[1, 2, 3] <class 'str'>

##1.4 eval()：去除引号的作用
# 1.4.1 可以实现list,dict.tuple.str之间的转换
print(1+23)
print('1'+'23')#123
print(eval('10+10'))#20,eval():执行运算，并返回运算值
'''
print(int('10+10'))#报错
#ValueError: invalid literal for int() with base 10: '10+10'

print(eval("10+'10"))#报错，整型和字符串不能相加
    10+'10
       ^
SyntaxError: unterminated string literal (detected at line 1)
'''

#1.4.2 str -> list
st1 = "[[1,2],[3,4],[5,6]]"
print(type(st1))#<class 'str'>
li = eval(st1)
print(li,type(li))
#[[1, 2], [3, 4], [5, 6]] <class 'list'>

#1.4.3 str -> dic
st2 = "{'name':'zcj','age':19}"
print(type(st2))#<class 'str'>
dic = eval(st2)
print(dic,type(dic))
#{'name': 'zcj', 'age': 19} <class 'dict'>

#1.4.4 eval非常强大，但是不够安全，不建议使用

##1.5 list():将可迭代对象转换为列表
# 支持转换为list的类型：str,tuple,dict,set

#str -> list
a1 = 'abcd'
a2 = list(a1)
print(list(a2),type(a2))
#['a', 'b', 'c', 'd'] <class 'list'>

#tuple -> list
print(list((1,2,3,4)))#[1, 2, 3, 4]

#dict -> list
print(list({'name':'zcj','age':19}))
#['name', 'age'],字典转为列表，会只取键名作为列表的值

#set -> list
print(list({'name','zcj','age','name'}))
#['name', 'zcj', 'age'],集合转换为列表会先去重
