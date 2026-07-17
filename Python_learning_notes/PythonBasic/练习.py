#（2）对字典 score = {"a": 5, "c": 2, "b": 8} 按值升序排序，返回排序后的键值对列表
score = {"a": 5, "c": 2, "b": 8}
items = score.items()
print(items) #返回一个视图对象，不是元组
print(type(items)) #<class 'dict_items'>
"""
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
