import time
from multiprocessing import Process
import os
###一,进程介绍

#1.含义
#操作系统进行资源分配的和调度的基本单位，是操作系统结构的基础
#一个正在运行的程序或者软件就是一个进程
#程序跑起来就成了进程
#注意：进程里面可以创建多个线程，多进程也可以完成多任务

#2.进程的状态
#（1）就绪：运行的条件已经满足，正在等待cpu执行
#（2）执行：cpu正在执行其功能
#（3）等待(阻塞)：等待某些条件满足，如一个程序sleep了，此时就处于等待状态
print("I am zcj") #程序开始，处于执行状态
sex = input("Please enter your gender：") #光标闪动，等待用户输入，处于等待状态
print(sex) #执行状态
time.sleep(1) #延时1秒，处于等待状态


###二,进程语法结构
#multiprocessing模块提供了Process类代表进程对象

#1.Process 类参数
#1）target：执行的目标任务名，即子进程要执行的任务
#2）args：以元组的形式传参
#3）kwargs：以字典的形式传参

#2.常用的属性
#name：当前进程的别名，默认Process-X
#pid: 当前进程的进程编号
def sing():
    print(f'sing子进程编号:{os.getpid()},sing父进程编号:{os.getppid()}')
    print('singing')
def dance():
    print(f'dance子进程编号:{os.getpid()},dance父进程编号:{os.getppid()}')
    print('dancing')
#os.getpid():获取子进程pid
#os.getppid():获取父进程pid


if __name__ == '__main__':
    #Create child processes （区别线程thread）
    p1 = Process(target=sing,name='child process111')
    p2 = Process(target=dance,name='child process222')
    #Start
    p1.start()
    p2.start()
    #访问name属性
    print(f'p1:{p1.name}   p1.pid: {p1.pid}')
    print(f'p2:{p2.name}   p2.pid: {p2.pid}')
    print(f"主进程的pid:{os.getpid()},主进程的父进程pid：{os.getppid()}\n")
'''
1.上面的是修改name属性的方法一
方法二：(有点像类)
p1.name = 'child process111'
p2.name = 'child process222'

2.运行结果
p1:child process111   p1.pid: 89712
p2:child process222   p2.pid: 132424
主进程的pid:122796,主进程的父进程pid：112236

sing子进程编号:89712,sing父进程编号:122796
singing
dance子进程编号:132424,dance父进程编号:122796
dancing

（1）if __name__ == '__main__':为主进程，主进程的父进程pid为pycharm的pid
（2）为什么子进程sing和dance的输出是在主进程之后？
主进程代码跑得更快，先执行完打印；子进程启动后要等系统调度 CPU，所以输出靠后。
'''

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

补充：if __name__ == '__main__':
1.防止别人导入文件的时候执行main里面的方法
2.防止windows系统递归创建子进程
'''

#4.进程中不共享全局变量
# 核心结论
# 不同进程拥有独立的内存空间，全局变量会在每个子进程中复制一份副本
# 子进程对全局变量的修改，只会作用在自身副本上，不会影响主进程和其他子进程

# 定义全局变量
num = 100

def work1():
    """子进程1：修改全局变量"""
    global num
    num += 10
    print(f"子进程1 pid:{os.getpid()}，修改后num = {num}")

def work2():
    """子进程2：读取全局变量"""
    print(f"子进程2 pid:{os.getpid()}，读取num = {num}")

if __name__ == '__main__':
    print(f"主进程 pid:{os.getpid()}，初始num = {num}")

    # 创建子进程
    p1 = Process(target=work1)
    p2 = Process(target=work2)

    # 启动子进程
    p1.start()
    p1.join()  # 等待p1执行完毕
    p2.start()
    p2.join()  # 等待p2执行完毕

    # 主进程再次打印全局变量
    print(f"主进程 pid:{os.getpid()}，最终num = {num}")

'''
主进程 pid:125960，初始num = 100
子进程1 pid:110560，修改后num = 110
子进程2 pid:122516，读取num = 100
主进程 pid:125960，最终num = 100

结果解析
1）全局变量num初始值为100，主进程内存中保存该值
2）创建子进程时，系统会把主进程的全局变量‘拷贝副本’给每个子进程
3）子进程1修改的是自己内存里的副本，主进程、子进程2的原始数据不受影响
4）最终主进程打印num，依然是最初的100，证明进程间全局变量不共享

4.补充对比（区分进程和线程）
# 线程共享同一块内存，多个线程可以直接修改同一个全局变量
# 进程内存相互隔离，天然不共享数据，如需进程间通信，要使用专门工具（队列、管道等）
'''

###三.进程间的通信
#1.导入模块
from queue import Queue

'''
1. from multiprocessing import Queue
定位：进程队列，多进程专属
使用场景：多进程之间数据传递（你的学习主线）
地位：多进程通信最常用、首选方案

2. from queue import Queue
定位：线程队列，标准库通用队列
使用场景：仅用于单进程内的多线程
禁忌：绝对不要用于多进程

3.补充区分记忆
多线程 → 用 queue 模块的 Queue
多进程 → 用 multiprocessing 模块的 Queue

4.可否同时导入？
结论：可以同时导入，但*会发生名称覆盖*，必须用别名区分，否则代码出错

（1）. 错误写法（直接同时导入，名称冲突）
from queue import Queue
from multiprocessing import Queue
后导入的 Queue 会覆盖前面的，最终 Queue 只代表 multiprocessing 里的队列

（2）. 正确写法：导入时指定别名（推荐）
from queue import Queue as ThreadQueue    # 线程队列，别名 ThreadQueue
from multiprocessing import Queue as ProcQueue  # 进程队列，别名 ProcQueue

'''
#2.队列的几个方法

# 队列构造参数：Queue(maxsize)
# maxsize：整数，代表队列最大存储元素个数
# （1）. maxsize <= 0  队列无大小限制，可无限存数据（默认情况）
# （2）. maxsize > 0   设置队列最大容量，存满后再put会阻塞等待

q = Queue(3) #最多接收三条消息
q.put("爱你到老")
q.put("你在做梦")
q.put("年轻人不讲武德")

print(q.full()) #True #判断队列是否满了
print(q.get()) #获取队列的一条消息，然后将其从队列中移除
print(q.get())

print(q.empty()) #False #判断队列是否为空
print(q.qsize()) #1 #返回当前队列包含的消息数量
print(q.full()) #False

print(q.get())
print(q.empty()) #True
print(q.qsize()) #0