def outer(m):
    print("outer()函数中的值:",m)
    def inner(n):
        print("inner()函数中的值:",n)
        return m+n
    return inner
ot = outer(10)
print(ot(20)) #第一次调用给inner()传值
# outer()函数中的值: 10
# inner()函数中的值: 20
# 30
#第二次调用内函数
print(ot(34))
# inner()函数中的值: 34
# 44

