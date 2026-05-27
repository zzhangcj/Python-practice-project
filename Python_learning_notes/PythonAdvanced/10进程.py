import time
from multiprocessing import Process
import os
# ###一,进程介绍
#
# #1.含义
# #操作系统进行资源分配的和调度的基本单位，是操作系统结构的基础
# #一个正在运行的程序或者软件就是一个进程
# #程序跑起来就成了进程
# #注意：进程里面可以创建多个线程，多进程也可以完成多任务
#
# #2.进程的状态
# #（1）就绪：运行的条件已经满足，正在等待cpu执行
# #（2）执行：cpu正在执行其功能
# #（3）等待(阻塞)：等待某些条件满足，如一个程序sleep了，此时就处于等待状态
# print("I am zcj") #程序开始，处于执行状态
# sex = input("Please enter your gender：") #光标闪动，等待用户输入，处于等待状态
# print(sex) #执行状态
# time.sleep(1) #延时1秒，处于等待状态
#
#
# ###二,进程语法结构
# #multiprocessing模块提供了Process类代表进程对象
#
# #1.Process 类参数
# #1）target：执行的目标任务名，即子进程要执行的任务
# #2）args：以元组的形式传参
# #3）kwargs：以字典的形式传参
#
# #2.常用的属性
# #name：当前进程的别名，默认Process-X
# #pid: 当前进程的进程编号
# def sing():
#     print(f'sing子进程编号:{os.getpid()},sing父进程编号:{os.getppid()}')
#     print('singing')
# def dance():
#     print(f'dance子进程编号:{os.getpid()},dance父进程编号:{os.getppid()}')
#     print('dancing')
# #os.getpid():获取子进程pid
# #os.getppid():获取父进程pid
#
#
# if __name__ == '__main__':
#     #Create child processes （区别线程thread）
#     p1 = Process(target=sing,name='child process111')
#     p2 = Process(target=dance,name='child process222')
#     #Start
#     p1.start()
#     p2.start()
#     #访问name属性
#     print(f'p1:{p1.name}   p1.pid: {p1.pid}')
#     print(f'p2:{p2.name}   p2.pid: {p2.pid}')
#     print(f"主进程的pid:{os.getpid()},主进程的父进程pid：{os.getppid()}\n")
# '''
# 1.上面的是修改name属性的方法一
# 方法二：(有点像类)
# p1.name = 'child process111'
# p2.name = 'child process222'
#
# 2.运行结果
# p1:child process111   p1.pid: 89712
# p2:child process222   p2.pid: 132424
# 主进程的pid:122796,主进程的父进程pid：112236
#
# sing子进程编号:89712,sing父进程编号:122796
# singing
# dance子进程编号:132424,dance父进程编号:122796
# dancing
#
# （1）if __name__ == '__main__':为主进程，主进程的父进程pid为pycharm的pid
# （2）为什么子进程sing和dance的输出是在主进程之后？
# 主进程代码跑得更快，先执行完打印；子进程启动后要等系统调度 CPU，所以输出靠后。
# '''

#3.方法
#1）start()：开启子进程
#2）is_alive():判断子进程是否还活着，存活返回True，死亡返回False
#3）join()：主进程等待子进程结束

def eat(name):
    print(f"{name}在干饭")
def sleep(name):
    print(f"{name}在睡觉")

if __name__ == '__main__':
    p1 = Process(target=eat,args=('bingbing',)) #注意这个逗号，元组里面只有一个元素的时候必须加
    p2 = Process(target=sleep,args=('ziyi',))
    p1.start()
    p1.join() #主进程处于等待状态，p1是运行状态
    p2.start()
    p2.join()
    print("p1存活状态：",p1.is_alive()) #p1存活状态： False
    print("p2存活状态：",p2.is_alive()) #p2存活状态： False
    #写在主进程中判断存活状态的时候需要加入join阻塞一下

'''
为什么不加join结果是Ture，加了之后则是False
join() 就是让主进程等子进程彻底运行完毕、自动退出；
等完再判断 is_alive()，子进程自然就是死亡状态。
没有join主进程就不会等一直运行走，这个时候子进程刚启动，自然是存活状态
'''


