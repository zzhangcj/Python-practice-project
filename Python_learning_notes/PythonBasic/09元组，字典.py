# ### 元组
# #1.元组名 = (元素1,元素2,元素3....)
# # tua = (1,2,3,'s')
# #元组内只有一个元素的时候，末尾要加逗号，否则返回唯一值的数据类型
# tub = (1,)
# print(type(tub))#<class 'tuple'>
# tub1 = ('d')
# print(type(tub1))#<class 'str'>
#
# ## 2.元组与列表的区别
# #元组只有一个元素的时候末尾必须加逗号，列表不需要
# #元组只支持查询操作，不支持增删改查
# li = [1,2,3]
# tua = (1,2,3,'s')
# print(tua[3])#元组也有下标，从左往右，从0开始
#
# #支持count(),index(),len(),in ,not in
# print(tua.index(3))#查找该元素下标
# print(tua.count(2))#查询出现次数
# print(len(tua))#查询元素总个数
#
# #3.应用场景
# #函数的参数和返回值
# #格式化输出后面的()本质上是一个元组
# name = "zcj"
# age  = 21
# print("%s的年龄是：%d" % (name,age)) #zcj的年龄是：21
# info = (name,age)
# print(type(info)) #<class 'tuple'>
# print("%s的年龄是：%d" % info) #zcj的年龄是：21
#
# #数据不可以被修改的时候保护数据
#
# ### 字典
# #1.基本格式：字典名 = {键1:值1,键2:值2....}
# #键值对保存，键和值之间用：隔开，每个键值对之间用 , 隔开
# dic = {"name":"zcj","age":21}
# print(type(dic)) #<class 'dict'>
# #字典中的键存在唯一性，但是值可以重复
# #键名重复时，不会报错，但是前面的值会被后面的值覆盖
#
# ## 2.字典的常见操作：增删改查
# #2.1查看：变量名[键名]
# #字典中没有下标，不能根据下标查找，要根据键名操作
# dic = {"name":"zcj","age":21,"gentle":"male"}
# print(dic['age'])
#
# #变量名.get(键名)
# print(dic.get('gentle'))
# print(dic.get('telephone'))#None 键名不存在返回None
# print(dic.get('telephone',"不存在"))
# #不存在 如果没有相应的键名，可以自己设置返回的值
#
# #2.2修改：变量名[键名] = 值
# dic1 = {"name":"jack","age":21,"gentle":"male"}
# dic1['age'] = 20 #字典通过键名来修改
# print(dic1)
# #已经有age键了，修改后面的值
#
# #2.3添加:变量名[新键名] = 值
# dic = {"name":"zcj","age":21,"gentle":"male"}
# dic['tel'] = 1234567 #没有tel键，新增进入字典
# print(dic)
#
# #2.4删除
# #del 删除整个字典:del dic
# #del 删除指定键值对，键名不存在会报错
# dic = {"name":"zcj","age":21,"gentle":"male"}
# del dic['gentle']
# print(dic)
# # del dic['telephone'] #报错
#
# #clear()：清空整个字典，但是保留这个字典
# dic = {"name":"zcj","age":21,"gentle":"male"}
# dic.clear()
# print(dic) #{} 空字典
#
# #pop():删除指定键值对，键不存在则报错
# dic = {"name":"zcj","age":21,"gentle":"male"}
# dic.pop('gentle') #和del的使用格式方法不一样
# print(dic)
# # dic.pop() #报错，里面没有键名
# #TypeError: pop expected at least 1 argument, got 0
# print(dic)
# dic.popitem()#默认删除最后一个键值对
# print(dic)


### 字典常见操作二
#3.1 len():求长度
dic = {"name":"zcj","age":21,"gentle":"male"}
print(len(dic)) #3,字典中有3个键值对

#3.2 keys():返回字典里面所包含的所有键名
dic = {"name":"zcj","age":21,"gentle":"male"}
print(dic.keys()) #dict_keys(['name', 'age', 'gentle'])
'''
for i in dic.keys():
    print(i)

等于[print(i) for i in dic.keys()]
'''

#3.3 values():返回字典里面包含的所有值
dic = {"name":"zcj","age":21,"gentle":"male"}
print(dic.values()) #dict_values(['zcj', 21, 'male'])

#3.4 items():返回字典包含的所有键值对，键值对以元组形式
dic = {"name":"zcj","age":21,"gentle":"male"}
print(dic.items())
#dict_items([('name', 'zcj'), ('age', 21), ('gentle', 'male')])
[print(i,type(i)) for i in dic.items()]#<class 'tuple'>

##字典的应用场景：使用键值对，存储描述一个物体相关的信息

### 集合
##1.基本格式：集合名 = {元素1,元素2,元素3,...}
s1 = {1,2,3}
print(type(s1)) #<class 'set'>
s2 = {} #这是一个空的字典，而不是集合
print(type(s2))#<class 'dict'>
s3 = set() #定义一个空集合
print(type(s3)) #<class 'set'>

##2.集合具有无序性
set1 = {'a','b','c','d','e','f'}
set2 = {1,2,3,4,5}
print(set1) #每次运行结果不一样
print(set2) #每次运行结果相同
#集合的无序性涉及hash表（了解）
print(hash('a'))
print(hash('b'))
print(hash('c'))
#同样的每次运行结果都不同，hash值不同，那么在hash表中位置也不同
#这样就实现了集合的无序性

print(hash(2))#2
print(hash(3))#3
print(hash(4))#4
#顺序不变
#python中int整型的hash值就是它本身，在hash表中的位置不会发生改变
#如果改成print(hash('2'))，变成字符串类型后，则hash值发生改变

#无序性：不能修改集合中的值

##3.集合具有唯一性，可以自动去重
set1 = {'a','b','c','e','e','a'}
print(set1) #{'c', 'a', 'b', 'e'}

### 集合的常见操作
##1.添加
#1.1 add()添加的为一个整体
s1 = {1,2,3,4,5}
print(s1)
s1.add(6)
print(s1)
#由于唯一性，如果添加的元素已经存在，则不进行任何操作
'''
s1.add(7,8)
print(s1) #一次只能添加一个元素
#TypeError: set.add() takes exactly one argument (2 given)
'''

s1.add((7,8))
print(s1)#{1, 2, 3, 4, 5, 6, (7, 8)}

#1.2 update 把传入的元素拆分，一个个放进集合中
s3 = {1,2,3,4}
print(s3)
s3.update([5,6,7])#这里用的列表，其实元组也可
#元素必须是能被for循环的可迭代对象
print(s3)#{1, 2, 3, 4, 5, 6, 7}

##2.删除
#2.1 remove():选择删除的元素，如果集合中没有，则报错
s4 = {1,2,3,4}
print(s4)
s4.remove(3)
print(s4) #{1, 2, 4}

#2.2 pop():
s5 = {1,2,3,4}
print(s5)
s5.pop()
print(s5)#{2, 3, 4}，删除的为第一个元素

s6 = {'a','b','c'}
print(s6) #因为无序性，结果随机
s6.pop()
print(s6) #但会默认删除第一个

#2.3 discard:选择要删除的元素，有则删除，没有则不会有任何操作
s7 = {1, 2, 3, 4, 5, 6, (7, 8)}
print(s7)
s7.discard((7,8))
print(s7) #{1, 2, 3, 4, 5, 6}

###交集和并集
##1.交集 &
a = {1, 2, 3, 4, 5, 6, (7, 8)}
b = {3,5,2}
c = {8,9,7}
print(a & b) #{2, 3, 5}
print(a & c) #set(),表示空集合

##2.并集 |

a1 = {'d','e','f'}
b1 = {'d','e','g','h'}
c1 = {8,9,7}
print(a1 | b1) #{'e', 'h', 'f', 'd', 'g'}
#重复的不算
print(a1 | c1) #{'e', 7, 8, 9, 'f', 'd'}

