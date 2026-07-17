''''''
# ## 1.给定字符串 s = " Hello Python World "，
# from idlelib.searchengine import search_reverse
#
# s = "  Hello Python World  "
# # 完成以下操作：
# # 去除字符串首尾空格
# s_strip = s.strip()
# print(s_strip)
# # 将所有字母转为小写，统计字母 o 出现的总次数
# s_lower = s.lower()
# print(s_lower)
# count_o = s_lower.count("o")
# print(count_o)
# # 按空格把字符串分割成单词列表，再用 - 拼接成新字符串
# word_list = s_strip.split()
# s_join = "-".join(word_list)
# print(s_join)
# # 把字符串中的 Python 替换为 Java
# s_replace = s_strip.replace("Python","Java")
# print(s_replace)
# # 用切片实现整个字符串反转\
# s_reverse = s_strip[::-1]
# '''
# [::-1] 三个参数全部用了省略写法，对应逻辑：
# start 省略：步长是 - 1（负数），所以默认从字符串最后一个字符开始
# end 省略：步长是 - 1，所以默认到字符串最开头结束（包含第一个字符）
# step = -1：步长为 - 1，也就是从右往左，每次往前走 1 位
# '''
#
# ##2.判断一个字符串是否是回文字符串（正读和反读完全一致，忽略大小写和非字母数字字符）。
# # 示例：输入 "A man, a plan, a canal: Panama"，返回 True；
# # 输入 "race a car"，返回 False
"""
# def is_palindrome(s:str) ->bool:
#     valid = [c.lower() for c in s if c.isalnum()]
#     return valid == valid[::-1]

"""

#
# ##3.给定列表，完成以下操作：
# nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
# # 在列表末尾添加元素 7，在索引为 2 的位置插入元素 0
# nums.append(7)
# nums.insert(2,0)
# # 删除第一个出现的元素 1，再删除索引为 3 的元素
# nums.remove(1)  #删除指定元素
# nums.pop(3)  #按索引删除元素
# # 分别实现：列表升序排序、降序排序、反转列表
# nums.sort() #升序
# nums.sort(reverse= True) #降序
# nums.reverse()
# # 用列表推导式筛选出列表中所有大于 3 的偶数
# filter_nums = [x for x in nums if x>3 and x%2==0]

#4（进阶高频）
# 实现列表去重，要求两种写法：
# 不保留元素原顺序（一行代码完成）
# 保留元素第一次出现的原顺序
# 示例：输入 [3,1,2,3,2,5]，第一种输出 [1,2,3,5]（顺序不定），第二种输出 [3,1,2,5]
def removeDuplicates(nums): #无序数组版本
    write = 0
    se = set()
    for read in range(len(nums)):
        if nums[read] not in se:
            se.add(nums[read])
            nums[write] = nums[read]
            write+=1
    return write

if __name__ == '__main__':
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = removeDuplicates(nums)
    print("不重复的元素个数：",res)
    print("去重后的数组：",nums[:res])#只是截取了nums的一部分，因为只改写了这部分

##5.元组
t = (10, 20, [30, 40], 50)
# 查找元素 50 的索引位置，统计元素 10 出现的次数
# print(t(1)) #TypeError: 'tuple' object is not callable  注意，()是函数调用
print(t[1]) #20
print(t.index(50)) #3
print((t.count(10))) #1
# 能不能直接修改元组第 0 位的元素？为什么？
# t[0] = 19 #TypeError: 'tuple' object does not support item assignment
#元组元素不可修改

# 能不能修改元组里的列表 [30,40]（比如给列表追加一个 50）？验证并说明原理
t[2].append(50)
print(t[2]) #[30, 40, 50]
print(type(t[2])) #<class 'list'>
# 可以修改，元组存的是列表的引用，引用不变，列表内部可变


##7.字典dict
d = {"name": "Tom", "age": 18, "city": "Beijing"}
# 添加键值对 "gender": "male"，修改 age 的值为 20
d["gender"]="male"
d["age"]=20
# 删除键 city，并获取被删除的值
city_val=d.pop("city") #Beijing
# pop()删除键值对，但同时会返回被删除的值
print(city_val)   # 输出: Beijing（被删除的值）
print(d) #{'name': 'Tom', 'age': 20, 'gender': 'male'}
# 分别遍历字典的所有键、所有值、所有键值对
for i in d.keys(): pass
# 遍历值
for j in d.values():pass
# 遍历键值对
for i,j in d.items():pass
# 用字典推导式生成一个字典：键是 1~5 的数字，值是对应数字的平方
square_dict = {i:i**2 for i in range(1,6)}



#8。字典进阶
# （1）合并两个字典 dict1 = {"a": 1, "b": 2} 和 dict2 = {"b": 3, "c": 4}
# 相同键保留 dict2 的值
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
# 合并方法1：update
merge1 = dict1.copy() #先复制一份 dict1
merge1.update(dict2) #将 dict2 的键值对"更新"到 merge1 中
"""
update() 直接修改调用它的字典（原地修改）
如果有重复键，dict2 的值会覆盖 dict1 的值
不返回新字典（返回 None）
"""

# 合并方法2：解包语法（Python3.5+）
merge2 = {**dict1, **dict2}
"""
1. **dict1 将字典"解包"成键值对
相当于：a=1, b=2

2. **dict2 将第二个字典也"解包"
相当于：c=3, d=4

3. 用花括号创建新字典，将所有键值对组合
merge2 = {"a": 1, "b": 2, "c": 3, "d": 4}

关键：
创建一个全新的字典,不修改原始字典
后面的字典会覆盖前面的（从左到右）
需要 Python 3.5+
"""

#（2）对字典 score = {"a": 5, "c": 2, "b": 8} 按值升序排序，返回排序后的键值对列表
score = {"a": 5, "c": 2, "b": 8}
sorted_score = sorted(score.items(), key=lambda x: x[1])


"""
score = {"a": 5, "c": 2, "b": 8}
items = score.items()
print(items)  
# dict_items([('a', 5), ('c', 2), ('b', 8)])
# 返回一个视图对象，不是元组
print(type(items))  # <class 'dict_items'>

1.items()的作用
items() 返回一个视图对象（dict_items,是可迭代的）
包含字典中所有的键值对元组
每个键值对是 (键, 值) 格式的元组

2.lambda x: x[1] 匿名函数

lambda 参数: 返回值表达式
lambda x: x[1]
# 等价于普通函数：
def get_value(x):
    return x[1]  # 返回元组的第二个元素（即值）

3.key = lambda x: x[1]
❌ 常见误解：key 函数返回的值直接赋值给 key
✅ 正确理解：key 是一个函数对象，使用时sorted() 内部调用 key(element)

4.sorted()
语法：sorted(iterable, key=None, reverse=False)
iterable-->要排序的可迭代对象（列表、元组、字典等）	--> ✅ 必需
key -->	指定排序依据的函数	--> 默认None
reverse -->	True=降序，False=升序	--> 默认False

5.sorted(score.items(), key=lambda x: x[1])你需要理解的
函数可以当作参数传递
key 参数接收一个函数
sorted() 会对每个元素调用这个函数
这个函数返回的值用来决定排序顺序
"""

