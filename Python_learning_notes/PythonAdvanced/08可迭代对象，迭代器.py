###一，可迭代对象Iterable
#遍历（迭代）：依次从对象中把一个个元素取出来的过程
#数据类型中可迭代的：str、list、tuple、dict、set等

#1.可迭代对象的条件
#1）对象实现了__iter__()方法
#2）__iter__()方法返回了迭代器对象

#2.for 循环工作原理
#1）先通过__iter__()获取可迭代对象的迭代器
#2）对获取到的迭代器不断调用__next__()方法来获取下一个值并将其赋值给临时变量i

#3.isinstance(o,t)方法：判断一个对象是否是可迭代对象或者是一个已知的数据类型
#o表示对象object
#t表示类型type，可以是直接或者间接类名，基本类型或元组
from collections.abc import Iterable
from typing import Iterator

"""
为什么要加 .abc？
因为从 Python 3.3 开始，官方把所有“用来判断类型” 的工具
都从 collections 移到了 collections.abc 子模块里。
"""
#3.1判断对象是否为可迭代对象
print(isinstance('123',Iterable)) #True
print(isinstance(123,Iterable)) #False
#3.2判断对象是否为其他类型，或者其中一种
print(isinstance(123,(str,tuple))) #False
print(isinstance(123,(int,dict))) #True

###二，迭代器
#是一个可以记住遍历位置的对象，在上次停留的位置继续去做一些事情

#1.案例
li = [1,2,3,4,5]
for i in li:
    print(i)


#2.iter()：调用对象的__iter__(),并把__iter__()返回的结果作为自己的返回值
l2 = iter(li)
print(l2) #<list_iterator object at 0x00000264ECDEF520>
print(li.__iter__()) #<list_iterator object at 0x000001CB6EE3FA00>
#iterator就是迭代器，iterator object就是迭代器对象

#3.next()：调用对象的__next__(),并把__next__()返回的结果作为自己的返回值
print(next(l2)) #1 print(li.__next__())效果和这里是相等的
print(next(l2)) #2
print(next(l2)) #3
print(next(l2)) #4
print(next(l2)) #5
#next()函数逐个取出元素
#如果再来一句print(next(l2)) ，由于已经取完元素，之后会引发StopIteration

#iter():可以获取到可迭代对象的迭代器
#next()：一个个去取元素，取完元素后会引发一个异常


#3.可迭代对象Iterable 和 迭代器Iterator
#凡是可以作用于for循环的都属于可迭代对象
#凡是可以作用于next()的都是迭代器


name = 'bingbing'
print(isinstance('bingbing',Iterable)) #True
print(isinstance('bingbing',Iterator)) #False
#可迭代对象不一定是迭代器对象
name2 = iter(name) #将name转换成迭代器对象
print(isinstance(name2,Iterable)) #True
print(isinstance(name2,Iterator)) #True
#迭代器对象一定是可迭代对象

#4.总结
# 可迭代对象可以通过iter方法转换为迭代器对象
#如果对象拥有__iter()__，是可迭代对象
#如果对象拥有__iter()__和__next__()方法，则为迭代器对象
#验证：使用dir()
print(dir(name))#能找到__iter()__，找不到__next__()
print(dir(name2))#__iter()__和__next__()都能找到

#5.迭代器协议（了解）
#对象必须提供一个next方法，执行该方法要么就返回迭代中的下一项，要么引发StopIteration异常，来终止迭代

#6.自定义迭代类
#两个特性：__iter()__和__next__()
class Test:
    #初始值为1，逐步增加1
    def __init__(self):
        self.num = 1
    def funa(self):
        print(self.num)
        self.num += 1
te = Test()
print(te)

for i in range(5):
    te.funa()#正常打印1，2，3，4，5

for i in te:
    te.funa()
    # TypeError: 'Test' object is not iterable


class MyIterator:
    def __init__(self):
        self.num = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.num == 10:
            raise StopIteration("终止迭代，数据被取完了")
        self.num += 1
        return self.num

mi = MyIterator()
print(mi) #<__main__.MyIterator object at 0x000002342976D550>
from collections.abc import Iterable
from typing import Iterator
print(isinstance(mi,Iterable)) #True
print(isinstance(mi,Iterator)) #True

for i in mi:
    print(i) #打印了1-10

'''
raise 主动抛出异常
raise StopIteration()作用：手动触发迭代终止信号
Python 捕获这个异常后，立刻结束 for 循环，不再取值

上面def __iter__(self)和def __next__(self)缺一不可，否则不能成为迭代器
这里和上面4.总结 相对应
'''

###三.生成器
#python中一边循环一遍计算的机制，叫做生成器

##1.生成器表达式
#1.1
for i in range(5):
    print(i*3)

#1.2
li = [i*3 for i in range(5)]
print(li) #[0, 3, 6, 9, 12]

#1.3
gen = (i*3 for i in range(5))
print(gen)
#<generator object <genexpr> at 0x00000274F6F7EF60>
print(isinstance(gen,Iterator)) #True
print(isinstance(gen,Iterable)) #True

#只是把这里的列表的[]变成()，就变成了生成器
for i in range(5):
    print(next(gen)) #结果和1.1相同

##2.生成器函数
#python中使用了yiel关键字的函数就称之为生成器函数

l1 = []
def test():
    # l1 = []
    l1.append("a")
    print("l1",l1)

test()
test()

#l1 = []的位置在函数内和函数外的最后test()结果是不一样的
#在内部的时候每一次test()都会重新生成l1列表
#如果要使l1 = []在test()内部使最后结果变得和在外部的时候，结果是一样的
#要使用生成器函数
def gen():
    print("start")
    yield 'a' #返回一个‘a'，并且暂停函数,下一次再从此处恢复执行
    yield 'b'
    yield 'c'

gen1 = gen()
print(isinstance(gen1,Iterator)) #True
print(isinstance(gen1,Iterable)) #True
print(gen1)
#<generator object gen at 0x00000245D9897580>
#使用了yield关键字，就是generator
print(next(gen1))
print(next(gen1))
print(next(gen1))

def gen2(n):
    print("\nHere is gen2")
    l2 = []
    for i in range(n):
        l2.append(i)
    print('l2:',l2)

gen2(3)

print(isinstance(gen2,Iterator)) #False
print(isinstance(gen2,Iterable)) #False
print('-' * 50)

print(gen2(4))
# Here is gen2
# l2: [0, 1, 2, 3]  ---因为使用了gen()，即调用了函数
# None ---函数没有return指定返回值，默认返回None

print(gen2) #function gen2
print('=' * 50)

def gen3(n):
    print("\nHere is gen33333")
    a = 0
    l3 = []
    while a < n:
        l3.append(a)
        yield a
        a += 1
    print('l3:',l3)

gen3(4)

print(gen3)#<function gen3 at 0x0000025BC8AAAD40>
print(isinstance(gen3,Iterator)) #False
print(isinstance(gen3,Iterable)) #False

print(gen3(4)) #<generator object gen3 at 0x000002167E583E60>
# 为什么这里也是调用gen3函数，却不执行打印结果？
# 调用函数不会立刻执行内部代码，只会创建并返回一个生成器对象，所以打印出来是生成器内存地址，不会立刻跑函数逻辑
print(isinstance(gen3(4),Iterator)) #True
print(isinstance(gen3(4),Iterable)) #True

for i in gen3(4):
    print(i)
'''
Here is gen33333
0
1
2
3
l3: [0, 1, 2, 3]

总结
1. yield 核心作用
（1）暂停 + 返回值：执行到 yield，送出数据（即yield 后面的东西），函数原地休眠
（2）断点续跑：下次取值，从暂停位置继续往后执行（执行next）
（3）不一次性生成全部数据，随用随取

2. 生成器实际用处
（1）节省内存：海量数据不用一次性存列表，取一个算一个，不会占满内存
（2）惰性执行：代码不调用不取数就不运行，按需计算
（3）简化迭代写法：不用手动写__iter__、__next__魔法方法

3. 三者关系
可迭代对象 ⊃ 迭代器 ⊃ 生成器
（1）可迭代对象
特征：拥有__iter__方法，没有__next__方法
作用：能被for循环遍历
示例：列表、元组、字符串、字典
特点：自身不一定能逐个取值，需借助迭代器读取

（2）迭代器
特征：同时有__iter__+__next__方法，__iter__返回自身
作用：具备逐个取出数据的能力，遍历到底自动终止
来源：可迭代对象调用iter()转换得到，自定义类实现魔法方法创建
特点：单向取值，取完无法回溯

（3）生成器
本质：特殊的迭代器
特征：函数内带yield关键字
作用：自带暂停续跑机制，按需产出数据
特点：惰性计算、占用内存极小，写法极简，不用手动写魔法方法

4.类比
（1）可迭代对象：一本书
整本书完整摆在这，想翻第几页都行，反复翻看多次也没问题。
例：列表[1,2,3]，循环多少次都能重新从头遍历。

（2）迭代器：一次性胶片放映机
胶片一张张往前播，放过的画面没法倒回去重放，播完一卷就空了。
取完一个数据就消耗掉，无法回溯重复读取。

（3）生成器：打印小票的收银机
不会提前把所有小票全部打印堆放，来一笔出一张，出完即作废；
按下yield按钮 = 收银机吐出一张小票（数据），然后自动暂停
下一次按下按钮（即调用 next()）机器从刚才暂停的地方继续打印下一张小票，不会重新从头打印
'''
