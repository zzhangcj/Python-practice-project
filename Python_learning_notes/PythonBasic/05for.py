### for循环
"""
for 临时变量 in 可迭代对象：
    循环体

"""

str = 'hellopython'
#可迭代对象就是要去遍历取值的整体，字符串是可迭代对象
# for i in str:
#     print(i)

#range()
#用来记录循环的次数，相当于一个计数器
# range(start,stop,step)
for i in range(1,6):#从1开始，到6结束，等于区间[1，6），6取不到
    print(i)# 结果为1，2，3，4，5
#range(4),结果从0到3，因为只写一个数字就是循环的次数，默认从0开始

#for循环应用：累加1-100
# s = 0
# for i in range(1,101):
#     s +=i
# print(s)
#与while循环相比，for循环更为简便，更为常见

# break：满足某一条件时，中途退出，结束循环
# continue：结束当前循环，进入下一循环
"""
 i = 1
 if i <= 5:
     print("I am eating apple")
     break #这里会报错，break和continue都只能放在循环内
"""


# i = 1
# while i <= 5:
#     print(f"小红在吃第{i}个苹果")
#     if i == 3:
#         print("吃饱了")
#         break # 结束break当前的循环
#     i += 1

i= 1
while i <=5:
    print(f"小明在吃第{i}个苹果")
    if i == 3:
        print(f"吃到一条虫子，第{i}个苹果不吃了")
        i += 1  # 在continue之前一定要修改计数器，否则会进入死循环
        continue ## 直接跳回 while 条件判断
        #立刻跳过本次循环剩下的代码，直接回到循环开头判断条件
    i += 1

for i in range(5):
    if i == 3:
        break #i=3的时候结束当前循环
    print(i)

for i in range(5):
    if i == 3:
        continue #跳过3，继续下一次循环
    print(i)
