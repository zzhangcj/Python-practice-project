### 1.字符串编码
#本质上时二进制数据与语言文字的一一对应关系

#Unicode：所有字符都是两个字节
#好处：字符和数字之间的转换速度更快一些
#坏处：占用空间大

#UTF-8:精准，对不同字符用不同的长度表示
#优点：节省空间
#缺点：字符与数字之间转换较慢，每次都要计算字符用多少个字节来表示

# ### 2.字符串编码转换
a = 'hello'
print(a,type(a))  #字符串是以字符为单位进行处理

a1 = a.encode()  #编码
print("编码后：",a1)
print(a1,type(a1))

a2 = a1.decode() #解码
print("解码后：",a2)
print(a2,type(a2))
#注意：对于bytes，只需要知道字符串类型之间的互相转换

print("\n")

st = "北凉徐凤年"
st1 = st.encode("utf-8")
print(st1,type(st1))
st2 = st1.decode("utf-8")
print(st2,type(st2))

### 字符串运算符
#1. + 字符串拼接
# print (10+10) #整型运算，这里的 + 表示算数运算
# print('10'+'10')#1010，这里的 +，表示字符串拼接
#
# name1 = "北凉"
# name2 = "徐凤年"
# print(name1+name2)
# print(name1,name2,sep="")#效果等同上面的
#
# #2. * 重复输出
# print("好好学习\n"*5)#需要输出多少次，*后面写多少
# print('&\t'*6)

### 字符串常见操纵
#作用：检查字符串中是否包含了某个子字符串
# """
# in：如果包含，返回True，不包含返回False
# not in：如果不包含，返回True，包含返回False
#
# """
#
# name = "北凉徐凤年"
#
# print("北" in name)        #True
# print("北" not in name)    #False
# print("徐凤年" in name)     #True
# print("徐龙象" in name)     #False
# print("徐龙象" not in name) #True
#
# ### 下标，索引
# #python中下标从0开始
# #作用：通过下标能够快速找到对应的数据
# #格式：字符串名[下标值]
#
# name = 'hello'
# i = 0
# for i in range(5):#取值的时候不要超过下标范围，否则会报错
#     print(name[i])
#     i +=1
#
# print(name[-1])#从右往左是从 -1 开始
# print(name[-2])
#
# ### 切片
# #含义： 对操作对象截取其中一部分
# #语法：[开始位置：结束位置：步长]
# #包前不包后，就是从开始位置开始，到结束位置前一位结束
# st = "北凉徐凤年"
# print(st[0:3]) #北凉徐 ,因为从0开始
# print(st[2:5]) #徐凤年
# #从右往左
# print(st[-1:]) #年
# print(st[:-1]) #北凉徐凤
#
# #步长：表示选取间隔，不写步长，默认为1
# #步长的绝对值大小决定切取的间隔，正负号决定切的方向
# #正数表示从左往右取值，负数表示从右往左取值
#
# print(st[-1::-1])   #年凤徐凉北
# print(st[:-1:-1])   # 啥也没有
# print(st[-1:-5:-1]) #年凤徐凉
# print(st[0:5:2])    #北徐年
