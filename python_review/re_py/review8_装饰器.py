""" 装饰器 Decorator """

'''一、概念简答题'''
# 什么是闭包？闭包的构成条件是什么？
'''
闭包是定义函数的时候的一种特殊结构，需要满足以下条件：
（1）函数嵌套(函数里面再定义函数)
（2）内层函数使用外层函数的局部变量
（3）外层函数的返回值是内层函数的引用
'''

# 装饰器的本质和原理是什么？为什么可以做到不修改原函数源码，就能给函数增加额外功能？
'''
装饰器本质是一个接收函数作为参数、返回新函数的高阶函数，基于闭包实现
它将原函数包装进内层 wrapper 函数，在 wrapper 里可以添加额外功能（日志、计时、权限校验），最终返回包装后的函数。
因为全程只是替换了函数引用，没有修改原函数的代码，所以做到了不改动源码增强功能
'''
'''
我的理解：
原有函数 A，想要扩展功能；定义函数 B，B 接收 A 作为参数。
B 内部定义 wrapper 函数，在 wrapper 中写新增逻辑，同时调用原函数 A；
B 返回 wrapper。此时 B 就是装饰器。
装饰器本质是函数，并且依靠闭包结构实现

return wrapper：向外交付 wrapper 函数对象，仅交付、不执行；
外层函数只在装饰绑定阶段运行一次；
后续调用 变量()，直接运行 wrapper，不会重新执行外层装饰器函数
'''


# @装饰器名 这个语法糖的本质是什么？
'''
@装饰器名 等价于 原函数 = 装饰器(原函数)，自动完成了函数替换，简化了写法
'''
'''
@装饰器 是语法糖，不是函数；
作用：自动执行 函数名 = 装饰器(函数名)；
左边函数名，被重新赋值
等号右侧 装饰器(函数名) 的返回值，就是装饰器 return 给到你的 wrapper 函数对象
'''

'''二、代码输出题
写出完整的执行顺序和打印结果'''

def outer(func):
    print("outer函数执行了")
    def wrapper():
        print("wrapper执行前")
        func()
        print("wrapper执行后")
    return wrapper

@outer
def foo():
    print("原函数foo执行")

foo()

'''三、编程实操题
编写一个装饰器 calc_time，可以统计被装饰函数的执行时间，
并打印函数名和耗时。（可使用 time 模块）'''
import time

def calc_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数 {func.__name__} 耗时：{end - start:.4f} 秒")
        return result
    return wrapper

# 测试
@calc_time
def test_func():
    time.sleep(1)

test_func()

#函数 test_func 耗时：1.0007 秒

'''
第 1 步：读到 @calc_time def test_func():
语法糖 @calc_time 等价于 test_func = calc_time(test_func)

第 2 步：执行 test_func()
现在 test_func 指向 wrapper，正式运行 wrapper 内部代码：
1. start = time.time() 记录开始时间
2. result = func(*args, **kwargs)
func就是最开始传进来的原始test_func，运行它；
time.sleep(1)休眠 1 秒；并且保存原函数返回结果
3. end = time.time() 记录运行完毕的时间
4. end-start 算出间隔，打印耗时
5. return result：把原函数的返回值往外返回

重点关键词通俗解释
1、 *args, **kwargs
作用：兼容任意参数的原函数。
不管原函数有多少位置参数、关键字参数，wrapper 都能原样转发给 func

2、func.__name__
获取原始函数的名字，打印日志更直观

3、 result = func(...) + return result
原始函数如果有返回值，我们必须接收并且返还，否则外部调用拿不到结果，功能出现 bug。

4、 为什么前面那道题没有return result？
场景 1：代码输出题
原始函数无业务返回数据，只做打印动作。
可以只写 func()，不用接收结果，不写return result暂时看不出问题。

场景 2：通用装饰器（比如之前的计时装饰器）
未来要装饰各式各样函数，很多函数会返回计算结果。
如果只写 func()，不捕获返回值、不向外 return，外部调用会丢失数据。
'''