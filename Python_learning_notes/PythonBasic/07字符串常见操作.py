# ### find()查找
# #作用：检测某个子字符串是否包含在字符串中
# #如果在就返回这个子字符串开始位置的下标，否则就返回-1
# #注意：开始和结束位置下标可以省略，表示在整个字符串中查找
#
# name = "北凉徐凤年徐龙象"
# print(name.find("凉"))# 1
# print(name.find("徐凤年"))# 2
# print(name.find("徐",3))# 5，从下标为3的地方开始find
# #这里其实我的代码写的是name.find("徐",3),sub,start是自动扩充的
# print(name.find("许")) # -1
# print(name.find("徐",4,6))#[4,6),包前不包后
# #name.find("徐",4,6),sub,start,end是自动扩充的
#
# ### index()
# #作用：检测某个子字符串是否包含在字符串中
# #如果在就返回这个子字符串开始位置的下标，否则就报错
# #index(子字符串，开始位置下标，结束位置下标)
# name = "我命由我不由天"
# print(name.index("命",2))
# #报错：ValueError: substring not found
#
# ### count()：返回某个子字符串在整个字符串中出现的次数，没有就返回0
# name = "北凉徐凤年徐龙象"
# print(name.count("徐"))#sub,start,end这些都一样
# print(name.count("许")) #没有，返回0

### 判断
#1.startswith()
#是否以某个字符串开头，是则返回True,否则返回False  sub,start,end这些都一样
name = "北凉徐凤年徐龙象"
print(name.startswith("凉"))# False
print(name.startswith("北凉"))# True
print(name.startswith("年",4,6))# True

#2.endswith()
#是否以某个字符串结尾，是则返回True,否则返回False  sub,start,end这些都一样
print(name.endswith("凉"))# False
print(name.endswith("龙象"))# True

#3.isupper():检测字符串中所有的字母是否都为大写，是则返回True
print(name.isupper()) #False
print("SIX".isupper())#True

### 修改元素
#1.replace():替换
#replace(旧内容，新内容，替换次数)
str = "好好学习，天天向上"
print(str.replace("天","每"))#好好学习，每每向上
#替换次数可省略，默认全部替换
print(str.replace("天","每",1))#好好学习，每天向上
# print(str.replace("天","每")) 其中old,new,count自动扩充的

#2.split():指定分隔符来切字符串
st = 'hello,python'
print(st.split(','))#['hello', 'python'],以列表的方式返回
#如果字符串不包含分割内容，就不会进行分割，会是一个整体
print(st.split('a'))#['hello,python']
print(st.split('o'))#['hell', ',pyth', 'n']
print(st.split('o',1))#['hell', ',python']，切割次数为1
#print(st.split('o',1)) sep,maxsplit分割次数，都是自动扩充

#3.capitalize():第一个字母大写，其他都小写
st = "bingBING"
print(st.capitalize())#Bingbing

#4.lower():大写字母转为小写
st = "bingBING"
print(st.lower())#bingbing

#upper():小写字母转为大写
st = "bingBING"
print(st.upper())#BINGBING
