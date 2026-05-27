# ###一.多任务
# import time
# from threading import current_thread
# #导入线程模块
# import threading
# from threading import Lock
#
#
#
# def sing():
#     print('I am singing')
#     time.sleep(2)
#     print("I have finished singing")
#
# def dance():
#     print("dancing")
#     time.sleep(2)
#     print("I have danced")
#
# sing()
# dance()
# #结果打印是按照一定的时间顺序的
#
# ###二.多线程
# #1.线程和进程
# #进程：是操作系统进行资源分配的基本单位，每打开一个程序至少就会有一个进程
# #线程：是cpu调度的基本单位，每一个进程都至少有一个线程，这个线程通常就是我们所说的主线程
#
# #一个进程默认有一个线程，进程里面可以创建多个线程，线程就是依附在进程里面的，没有进程就没有线程
# #多线程就是同时运行多个线程
#
#
# #2.Thread线程参数
# # target：执行的任务名
# # args:以元组的形式给任务传参
# # kwargs:以字典的形式给任务传参
# def sing1(name1):
#     print(f'{name1} am singing, (1)')
#     time.sleep(2) #time.sleep(n) # n 是数字，代表暂停 n 秒
#     print(f"{name1} have finished singing, (2)")
#
# def dance1(name2):
#     print(f"{name2} is dancing, (3)")
#     time.sleep(2)
#     print(f"{name2} have danced, (4)")
#
# #主程序入口
# if __name__ == '__main__':
#     #1.创建子线程
#     t1 = threading.Thread(target=sing1,args=('zcj',))#args必须传元组，单元素要加逗号
#     t2 = threading.Thread(target=dance1,args=('zcj',))
#
#     #3.守护线程，必须放在start前面：主线程执行结束，子线程也会跟着结束
#     t1.daemon = True
#     t2.daemon = True
#
#     #2.开启子线程
#     t1.start()
#     t2.start()
#     #结果(1)和(3)同时出来，然后(2)(4)同时出来
#
#     #4.阻塞主线程join()：暂停的作用，等子线程执行结束，主线程才会继续执行，必须放在start后面
#     t1.join()
#     t2.join()
#
#     #6.更改线程名字
#     t1.name = "子线程一"
#     t2.name = "子线程二"
#
#     #5.获取线程名字
#     print(t1.name)
#     print(t2.name)
#
#     print("\nPerfectly concluded,the performance has ended!")
#
#
# ##3.线程之间执行是无序的
# #线程执行是根据cpu调度决定的
# def task():
#     time.sleep(1)
#     print("当前线程为：",threading.current_thread())
#
# if __name__ == "__main__":
#     for i in range(5):
#         #每循环一次，创建一个子进程
#         t = threading.Thread(target=task)
#         #启动子进程
#         t.start()
# #结果打印十分混乱的原因：
# #线程并发抢占CPU，5个线程休眠结束后抢着打印，输出顺序不固定。控制台打印缓冲争抢，文字交错错乱
#
# #4.线程之间共享资源
# li = []
# #写入数据
# def wdata():
#     for i in range(5):
#         li.append(i)
#         time.sleep(1)
#     print("The data written is:",li)
#
# def rdata():
#     print("The data read is:", li)
#
#
# if __name__ == '__main__':
#     #创建子进程
#     wd = threading.Thread(target=wdata)
#     rd = threading.Thread(target=rdata)
#     #开启子进程
#     wd.start()
#     wd.join()
#     rd.start()
#     rd.join()
#
# #5.资源竞争
# a = 0
# b = 1000000
# def add():
#     for i in range(b):
#         global a
#         a += 1
#     print("The first add:",a)
#
#
# def add2():
#     for i in range(b):
#         global a
#         a += 1
#     print("The second add:", a)
#
#
# if __name__ == '__main__':
#     a1 = threading.Thread(target=add)
#     a2 = threading.Thread(target=add2)
#
#     a1.start()
#     a2.start()
#     #b的数字足够大，add的值是随机的，add2的结果是固定的
#     #使用join()阻塞，等待a1子线程执行结束，代码再往下运行，开始a2子线程就可以保证结果没问题
#
# """
# global a
# #函数里修改全局变量，必须先用global声明；只读取不用改就不用写。
# 不加 global a 运行会报：
# UnboundLocalError: local variable 'a' referenced before assignment
# 分步解释:a = 0 是全局变量
# 函数里写了 a += 1，属于赋值修改操作
# Python 规则：函数内只要出现对变量赋值，解释器就默认它是局部变量
# 没声明全局，又提前用到这个局部变量，直接报错
#
# 资源竞争
# 为什么 b的数字足够大，add的值是随机的，add2的结果是固定的
# 1.单线程顺序执行
# 先跑完add再加 100 万，再跑add2再加100万，最终结果固定为2000000
# 2.多线程并发执行
# 两个线程同时抢着修改全局变量a，a += 1实际分三步：
# 读取 a 值 → 计算 + 1 → 赋值回 a
# 线程互相插队覆盖数据，最终结果小于 2000000，数值随机不固定。
# 3.总结
# 全局变量会被所有线程共享
# 多线程同时修改共享数据，会出现数据错乱、计算不准
# 这就是线程安全问题，后续要用线程锁解决争抢问题
# """
#
# #6.线程同步
# #主线程和创建的子线程之间各自执行完自己的代码直到结束
# # a1.start()
# # a2.start() #这里是上面的代码
# # 使用join()阻塞，等待a1子线程执行结束，代码再往下运行，开始a2子线程就可以保证结果没问题
# '''
# 总结：
# join() 是最简单的线程同步手段，作用：让线程排队执行，避免争抢数据。
# 不加 join：并发争抢（不同步）
# 加 join：串行同步（有序执行）
# join() 强行控制线程执行顺序，达成线程同步，解决多线程抢数据问题。
# 真正严谨的同步后期用线程锁 Lock，join 只是简易同步方式。
# '''
#
# ##7.互斥锁
# #对共享数据进行锁定，保证多个线程访问共享数据不会出现数据错误的问题
# #保证同一时刻只能有一个线程去操作
#
# #导入模块
# from threading import Lock
# #(1)创建全局互斥锁
# lock = Lock()
# a = 0
# b = 1000000
# def add3():
#     #(2)上锁
#     lock.acquire()
#     for i in range(b):
#         global a
#         a += 1
#     print("The first add:",a)
#     #(3)释放锁
#     lock.release()
#
#
# def add4():
#     lock.acquire()
#     for i in range(b):
#         global a
#         a += 1
#     print("The second add:", a)
#     lock.release()
#
#
# if __name__ == '__main__':
#     a3 = threading.Thread(target=add3)
#     a4 = threading.Thread(target=add4)
#
#     a3.start()
#     a4.start()
# # The first add: 1000000
# # The second add: 2000000
#
# '''
# 注意：acquire和release必须成对出现，否则可能出现死锁
# 互斥锁总结
# 1. 核心作用：锁定共享数据，同一时刻仅允许单个线程读写修改，避免多线程资源争抢，保障运算结果准确。
# 2. 使用规范：加锁与解锁必须成对匹配使用，缺一不可。
# 3. 死锁问题：线程互相僵持、持续等待对方释放锁，程序卡住无响应，无法正常执行后续任务。
# 4. 性能弊端：线程由并行变为串行排队执行，会降低程序整体运行效率。
# 5. 适用场景：多线程并发操作全局共享变量、公共数据时使用。
# '''
#
#
#
#
###三.线程特点
#1.线程之间共享资源（全局变量）
import time
from threading import Thread

l1 = []
#写入数据
def wdata():
    for i in range(5):
        l1.append(i)
        time.sleep(0.2)
    print("The data written is:",l1)
#读取数据
def rdata():
    print("The data read is:",l1)

if __name__ == "__main__":
    #Create child threads
    t1 = Thread(target=wdata)
    t2 = Thread(target=rdata)
    #Start child threads
    t1.start()
    #Blocked thread
    t1.join() #加了join()这个方法就会等待t1任务执行结束，不加的话t2跑得比t1块，会出现读取不全的情况
    #time.sleep(n) #n是某个数字，看前面的0.2，n=0.2x时，可以读取x个数据
    t2.start()
    t2.join() #这里要不要加t2.join？
    print("The main thread ends")

'''
这里要不要加t2.join？

不加：
The data written is: [0, 1, 2, 3, 4]
The data read is:The main thread ends 
[0, 1, 2, 3, 4]

t2 子线程还在运行时，主线程就结束了；
但Python 主线程退出不会强行杀死子线程，子线程依然会跑完，只是主线程先结束。
所以打印的"The main thread ends"不在结尾，后面还有读取到的东西

加上：
The data written is: [0, 1, 2, 3, 4]
The data read is: [0, 1, 2, 3, 4]
The main thread ends

所有子线程全部执行完成，主线程才收尾退出，所以打印的"The main thread ends"正常在末尾
'''
































