###列表
#1.基本信息
#列表名 = [元素1,元素2,元素3....]
#元素之间用 , 隔开，元素得在[]内
#元素之间的数据类型可以不同

# li = [1,2,'three','哈哈']
# print(li,type(li))
# #列表可以进行切片操作
# print(li[0:3])
# #列表是可迭代对象，可以用for循环遍历取值
# for i in li:
#     print(i)
#
# ### 2.列表添加操作
# #append(),extend(),insert()
#
# li = ['one','two','three']
# li.append('four') #apppend():整体添加
# print(li) #['one', 'two', 'three', 'four']
#
# li.extend('five')
# print(li)#extend 分散添加，将另外一个类型的元素逐一添加
# #['one', 'two', 'three', 'four', 'f', 'i', 'v', 'e']
#
# #li.insert(3,'four')
# li.insert(3,'4')#insert 指定位置添加元素
# #指定位置如果有元素，原有元素会后移
# print(li)
#
# li = [1,2,3,4]
# li.append(5)
# li.extend(5)#TypeError: 'int' object is not iterable
# #这里是因为5为整型，不可分割
# li.insert(5,6)
# print(li)

# ### 3.修改,查找
# #修改：直接通过下标就可以进行修改
# li = [1,2,3]
# li[1] = 'a'
# print(li) #[1, 'a', 3]
#
# #查找：in , not in
# #in:判断指定元素是否存在列表中，存在则返回True，不存在返回False
# #not in:与in 相反
# li = [1,2,3]
# print(3 in li)#True
#
#
# """
# 选中代码按tap,会帮你自动调整缩进
# """
# #用户输入昵称，重复则不可用，定义列表，保存已有的昵称
# name_list = ['jack','zcj','zmgjjkk']
# while True:
#     name = input("请输入你的昵称：")
#     #判断昵称是否已经存在
#     if name in name_list:
#         print(f"你输入的昵称{name}已经存在")
#     #如果昵称不存在
#     else:
#         print(f"昵称{name}已经被你使用")
#         name_list.append(name)
#         #昵称新增到列表
#         print(name_list)
#         break

#index 返回指定数据所在位置的下标，如果数据不存在则报错
#count 统计指定数据在列表中出现的次数
### 4.删除
# del
li = [1,2,3,'a']
# del li #表示删除整个列表
del li[3]
print(li)#[1, 2, 3]

#pop()
li.pop()#默认删除最后一个元素
print(li)#[1, 2]

li = [1,2,3,'a']
li.pop(2)#不能指定删除2，只能根据下标进行删除，这里是删除3
print(li)#[1, 2, 'a']

#remove:根据元素的值来删除，可指定删除
li = [1,2,3,'a','a']
li.remove('a')
print(li)#[1, 2, 3, 'a']
#不会删除所有指定元素，默认删除最开始出现的一个
#列表中不存在指定的元素则会报错

###5.排序
#sort: 将列表按特定顺序重新排序，默认从小到大
li = [2,3,1,8,5,4]
li.sort()
print(li)#[1, 2, 3, 4, 5, 8]

li.reverse()#将列表倒序，而不是从大到小
print(li)#[8, 5, 4, 3, 2, 1]

###6.列表推导式
#格式1：[表达式 for 变量 in 列表]
#注意：in后面不仅可以放列表，还可以放range(),可迭代对象
li = [1,3,9,4,5]
[print(i*2) for i in li]#将列表中元素每个都乘以2

li = []
for i in range(1,5):
    li.append(i)
print(li) #[1, 2, 3, 4]

li = []
[li.append(i) for i in range(3,7)]
print(li) #[3, 4, 5, 6]

#格式2：[表达式 for 变量 in 列表 if 条件]
li = []
for i in range(1,14):
    if i % 2 == 1:
        li.append(i)
print(li) #[1, 3, 5, 7, 9, 11, 13]

li = []
[li.append(i) for i in range(1,11) if i % 2 == 1]
print(li) #[1, 3, 5, 7, 9]

###7.列表嵌套
#一个列表里面可以有另一个列表
li = [1,2,3,['a', 1,'ff']]
print(li[3])    #['a', 1, 'ff']
print(li[3][2]) #ff
#取出内列表中的元素
