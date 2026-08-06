import threading
from threading import Lock         # 互斥锁，最常用，同一时间只允许一个线程执行
import time
"""知识点复习：from import
import threading
把整个 threading 模块导入
之后你要用里面东西得写全名

from threading import Lock
从 threading 模块里面，单独把 Lock 这个类拿出来，放到当前命名空间。
之后直接写 Lock() 就可以，不用写 threading.Lock()
"""

"""一、概念简答题
1、Python 中创建多线程有哪两种常用方式？
方式一：实例化 threading.Thread 对象，通过 target 参数传入目标函数，args 传参
方式二：自定义类继承 Thread，重写 run () 方法，实例化后调用 start () 启动

（方式一，详见09线程，多线程，互斥锁.#2.Thread线程参数）

（方式二解析
相当于改造官方自带的 Thread，自己做一个子类
run 这个方法原本官方 Thread 就自带，现在我们要跑自己的业务逻辑，所以就要重写 run。
我们自己代码不要直接去调用 run，只需要实例化对象，调用 start ()，它内部就会自动帮我们调用重写后的 run）
"""

"""2、join() 方法的作用是什么？不调用 join 的话，主线程和子线程的执行顺序是怎样的？
让主线程阻塞等待，直到调用 join 的子线程执行完毕后，主线程才继续往下执行。
不调用 join：主线程不会等待子线程，启动子线程后立刻继续执行后续代码；
主线程执行完后会等待所有普通子线程结束，程序再退出
"""

'''3、多个线程同时修改全局共享变量时，为什么会出现数据错乱？加Lock互斥锁为什么能解决这个问题？
(资源竞争，详见09线程，多线程，互斥锁.#5.资源竞争)

count += 1不是原子操作，会被拆分为「读取 count → 计算 + 1 → 写回 count」三步
GIL 在线程间切换时，可能两个线程都读到旧值，写回后覆盖对方的结果，导致最终计数偏少
Lock 解决原理：加锁后同一时刻只有一个线程能进入临界区（修改共享变量的代码），保证操作原子性，避免数据竞争
'''

'''4、Python 多线程适合什么类型的任务？为什么不适合 CPU 密集型任务？
适合：IO 密集型任务（网络请求、文件读写、数据库查询）
不适合：CPU 密集型（大量计算、循环运算、数据处理）
'''

"""二、代码输出题
写出下面代码的大致输出结果（说明打印顺序即可），并解释原理"""
def task(name):
    print(f"{name} 启动")
    time.sleep(1)
    print(f"{name} 结束")

if __name__ == '__main__':
    t1 = threading.Thread(target=task, args=("线程1",))
    t2 = threading.Thread(target=task, args=("线程2",))
    t1.start()
    t2.start()
    print("主线程执行完毕")

"""原理
t1.start()、t2.start()：开启两个子线程，子线程马上执行 task 函数打印「xx 启动」，然后进入 time.sleep(1) 睡眠
主线程不会阻塞等待，start 之后直接往下执行，打印主线程执行完毕。
主线程打印完，主线程自身代码跑完；但没有 join，程序不会退出，继续等待这两个非守护子线程。
睡眠 1 秒到期，两个子线程分别打印结束。两个结束的先后顺序操作系统随机
"""

'''三、代码改错题
下面的代码期望两个线程各累加 100 万次，最终count等于 2000000
但实际运行结果总是小于 2000000。请指出问题原因，并写出修改后的正确代码'''

import threading

count = 0

def add():
    global count
    for _ in range(1000000):
        count += 1

t1 = threading.Thread(target=add)
t2 = threading.Thread(target=add)
t1.start()
t2.start()
t1.join()
t2.join()
print(count)


import threading

count = 0
lock = threading.Lock()  # 创建互斥锁

'''答案：加上with lock
for _ in range(1000000):
    with lock:  # 操作共享变量前加锁
        count += 1


1。lock用法
先回忆 Lock 的原始写法（不用 with）
lock.acquire()   # 🔒上锁：抢到锁才能往下执行，抢不到就阻塞等待
count += 1
lock.release()   # 🔓释放锁，别的线程才有机会拿到锁

acquire()：加锁
release()：解锁
坑点： 如果 count +=1 中间代码抛出异常，release() 不会执行 → 锁永远不释放，程序卡死死锁


2.with用法
with 通用概念（不只是锁，面试常考）
with 叫上下文管理器，不止用于锁。
文件操作你肯定见过：

# 自动打开，离开with自动close关闭文件，不用手动f.close()
with open("a.txt","r") as f:
    data = f.read()
    
通用逻辑：
with 对象:
    代码块
    
    
3.等价写法
with lock:
    count += 1
等价于
lock.acquire()
try:
    count += 1
finally: #特点：无论是否报错，finally必定执行释放。杜绝忘记 release 造成死锁
    lock.release()
    
核心两点
    进入 with 代码块的时候，自动执行 lock.acquire() 上锁
    离开 with 代码块（不管正常走完，还是中途报错异常），一定会执行 lock.release() 释放锁
    
4.每次循环
    （1）with lock → acquire 拿到锁
    （2）执行 count +=1（共享变量，受锁保护，同一时刻只允许一个线程在这里执行）
    （3）缩进结束，离开 with 块 → 自动 release 释放锁，下一个线程才有机会进来修改 count
    
⚠️注意范围！
# 正确：只把共享变量操作放with里面(这一点很重要)
with lock:
    count +=1
    
不要写成这样（锁包住整个循环，变成完全串行，多线程失去意义）
# ❌不好，整个循环被锁，退化成单线程
with lock:
    for _ in range(1000000):
        count +=1
'''

'''四、场景分析
你正在开发一个网络爬虫，需要并发下载 100 个网页。你会选择多线程还是多进程？为什么？请给出简单的多线程实现伪代码。
'''
import threading
import requests

import threading   # 导入线程模块，用于创建多线程实现并发
import requests    # 网络请求库，发送HTTP请求下载网页


def download(url):
    """单个线程执行的函数：下载一个网页"""
    resp = requests.get(url)   # 发送网络请求，大部分时间在等待网络IO响应
    print(f"完成下载：{url}，长度：{len(resp.text)}")  # resp.text获取网页文本，len统计字符数


if __name__ == "__main__":
    # 程序入口：直接运行本文件才执行下面代码，被导入时不执行
    url_list = ["url1", "url2", "url3"]  # 存放100个待下载的网页地址（这里只写了3个）

    thread_list = []  # 空列表，用来保存所有线程对象，后续用来等待线程结束

    # 循环：为每一个网址创建并启动线程
    for url in url_list:
        # 创建线程对象；target指定执行函数(不要加括号!)，args传参必须是元组，单个参数末尾逗号不能少
        t = threading.Thread(target=download, args=(url,))
        thread_list.append(t)  # 把线程存入列表保存
        t.start()              # start()真正启动子线程，开始执行download函数

    # join：主线程阻塞，等待每一个子线程全部执行完毕
    for t in thread_list:
        t.join()

    print("全部网页下载完毕")
