""""""
import  gevent #导入模块
import time
#
# ###一.携程
# #含义：单线程下的开发，又称为微线程
# #注意：线程和进程的操作是程序触发系统接口，最后的执行者是系统，协程的操作则是程序员
#
# #1.简单实现协程
# """
# yield复习：
# 1.基本概念
# 函数里出现 yield → 调用函数不执行函数体，直接返回生成器对象
# next(生成器) / for 迭代时，函数运行到 yield，暂停，把 yield 后的值当作返回值
# 再次next()，从上次yield暂停位置继续往下跑
# 2.核心功能
# （1）按需惰性生成数据（节省内存）
# 普通return一次性构造完整列表存入内存；yield逐个产出、用一个算一个
# （2）暂停 / 恢复函数执行（协程基础）
# yield可以挂起当前函数上下文（局部变量、运行位置保存），切换其他代码运行，是简易协程实现基础
# 3.return 和 yeild的对比
# return：终止函数，一次性返回，销毁局部变量
# yield：暂停函数，返回数据，保留上下文，后续可继续执行
# """
# import time
# def task1():
#     while True:
#         yield 'hahaha'
#         time.sleep(1)
#
#
# def task2():
#     while True:
#         yield 'hehehe'
#         time.sleep(1)
#
#
# if __name__ == "__main__":
#     t1 = task1()
#     t2 = task2()
#     while True:
#         print(next(t1))
#         print(next(t2))
#
# #现象：交替打印 hahaha /hehehe，两个任务在同一个主线程来回切换执行 → 并发
# #协程本质：单线程内多个子程序互相让出 CPU、切换执行，用户态调度，无内核切换开销
#
# #2.协程应用场景
# #（1）如果一个线程里面IO操作比较多的时候，可以用协程
# #IO：Input/Output，常见的IO操作有 文件操作，网络请求
# #（2）适合高并发处理
#
# ###二.greenlet
# #一个由C语言实现的协程模块，通过设置switch()来实现任意函数之间的切换
# #注意：greenlet属于手动切换，当遇到IO操作，程序会阻塞，而不能自动切换
#
# #1.通过greenlet实现任务切换
# from greenlet import greenlet
# def sing():
#     print("I am singing")
#     g2.switch()
#     print("I have finished singing")
#
# def dance():
#     print("I am dancing")
#     print("I have finished dancing")
#     g1.switch()
#
# if __name__ == "__main__":
#     #创建协程对象：green(任务名)
#     g1 = greenlet(sing)
#     g2 = greenlet(dance)
#     g1.switch() #切换到g1中去
#     g2.switch()
#
# ###三.gevent：遇到IO操作时，会进行自动切换，属于主动式切换
# #1.注意：文件命名不要和第三方模块或者内置模块重名
#
# #2.使用
# #gevent.spawn(函数名)：创建协程对象
# #gevent.sleep(): 耗时操作
# #gevent.join():阻塞，等待某个协程执行结束
# #gevent.joinall(): 等待所有协程对象都执行结束再退出，参数是一个协程对象列表
# def sing1():
#     print("I am singing")
#     gevent.sleep(2)
#     print("I have finished singing")
#
# def dance1():
#     print("I am dancing")
#     gevent.sleep(3)
#     print("I have finished dancing")
#
# if __name__ == "__main__":
#     g1 = gevent.spawn(sing1)
#     g2 = gevent.spawn(dance1)
#     #阻塞，等待协程执行结束
#     g1.join()
#     g2.join()
#
#
# """
# 1.运行结果
# I am singing
# I am dancing  #等2s → sing结束
# I have finished singing #再等1s → dance结束
# I have finished dancing
#
# （如果都改为time.sleep()则总耗时5s）
#
# 2.核心知识点
# gevent.sleep()是模拟 IO 阻塞（网络 / 文件等待），遇到它自动切其他协程：
# sing 休眠 2 秒时，CPU 不等待，立刻跑去执行 dance；
# 总耗时≈3 秒（串行要 2+3=5 秒），直观体现协程并发
# """
#
#3.joinall()
def sing2(name):
    for i in range(1,4):
        gevent.sleep(1)
        print(f"{name}在唱歌，被送走第{i}次")

if __name__ == "__main__":
    gevent.joinall([
        gevent.spawn(sing2,"bingbing"),
        gevent.spawn(sing2,"冰冰")
    ])
#joinall():等待所有的协程都执行结束再退出
"""
1.原理
列表里所有协程同时启动、并发运行，joinall只负责阻塞主线程，等列表里所有协程全部运行结束，代码才往下走

2.对比join
g.join()：主线程阻塞，等待当前这一个协程执行完毕
gevent.joinall([g1,g2,...])：全部协程并发执行，主线阻塞直到全部完成

3.sleep：模拟阻塞
gevent.sleep(1):耗时3s，bingbing和冰冰同时唱歌
time.sleep(1):耗时6s，bingbing先唱3次，冰冰再唱3次
"""

#3.4 monkey补丁：拥有在魔魁啊运行时替换的功能
from gevent import monkey
monkey.patch_all() #将用到的time.sleep()代码替换为gevent里面自己实现耗时操作的gevent.sleep()代码
#注意：monkey.patch_all()必须放在被打补丁者前面
def sing3(name):
    for i in range(1,4):
        time.sleep(1)
        print(f"{name}在唱歌，被送走第{i}次")

if __name__ == "__main__":
    gevent.joinall([
        gevent.spawn(sing3,"zmjjkk"),
        gevent.spawn(sing3,"ddy")
    ])

###四.总结
#1.线程时CPU调度的基本单位，进程是资源分配的基本单位
#2.进程，线程，协程对比
# （1）. 进程：资源分配单位，内核调度切换，资源隔离，开销最大；CPU密集首选
# （2）. 线程：CPU调度单位，内核切换，同进程共享资源，开销中等；IO密集可用，受GIL限制无法多核跑计算
# （3）. 协程：用户态切换，单线程内并发，资源开销最小；IO密集最优，无GIL影响、无需锁
#3. 选用规则：
#    CPU密集 → 多进程
#    IO密集(爬虫、文件、网络) → 多线程/协程
