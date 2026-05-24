# if
score = input('请输入你的成绩：')
if score == '100':
    print('你真棒！')
if score == '60':
    print('还要继续加油！')

### 比较（关系）运算符
# == 比较两个变量的值是否相等，相等就返回为True,不等返回False
# != 比较两个变量的值是否不相等，不相等就返回为True,相等返回False
# 同理，大于小于也一样

### 逻辑运算符
# and: 左右两边都符合才为真
# or : 左右两边有一个符合就为真
# not: 表示相反的结果
print(not 3>9)#最后输出为True

### 三目运算（三元表达式）
#基本格式： 为真结果 if 判断条件 else 为假结果

#if-else 二选一
a = 666
b = 999
if a <= b:
    print('a小于等于b')  #结果为真
else:                #else后面不需要添加任何条件
    print('a比b大')     #结果为假
#三目运算（三元表达式）
print('a小于等于b') if a <= b else print('a比b大')

#if-elif 多选一
"""
if 条件1：
    满足条件1要做什么
elif 条件2：
    满足条件2要做什么
elif 条件3：
    满足条件3要做什么
"""
score  = 88
if 85 <= score <= 100:
    print('优秀')
elif 60 <= score <= 80:
    print('及格')
elif 0 <= score <= 60:
    print('不及格')
else:
    print('成绩无效')

#if嵌套：if里面也有if
"""
if 条件1：
    满足条件1要做什么
    if 条件2：
        满足条件2要做什么
else：
    不满足条件要做什么
"""
#注意：内层if判断和外层if判断都可以是if-else结构
ticket= True
tem = 38.5
if ticket == 1:
    print("可以进站了")
    if 36.3 <= tem <= 37.3:
        print("体温正常")
    else:
        print("体温异常，被抓去隔离")
else:
    print("没票不能进站")
