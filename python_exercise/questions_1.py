# #1
# l = []
# for i in range(2000,3201):
#     if (i%7==0) and (i%5!=0):
#         l.append(str(i))
# print(','.join(l))
# #.join(可迭代对象) 是字符串自带方法
# #作用：用当前字符串作为分隔符，拼接列表里所有元素

#2
def fact(x):
    if x == 0:
        return 1
    return x*fact(x-1)
print("请输入一个数字：")
x = int(input())
print(fact(x))

#3
print("请输入一个数字n:")
n = int(input())
dic = {}
for i in range(1,n+1):
    dic[i] = i*i