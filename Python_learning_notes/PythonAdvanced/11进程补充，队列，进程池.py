import time
from multiprocessing import Process
import os
from multiprocessing import Queue
'''
========== 以下为新增补充知识点 ==========
补充1：if __name__ == '__main__':
(你要写很多函数，写一个测试一个看看写的这个对没有)

一、通用作用（所有Python代码适用）
1.区分运行身份
直接运行当前文件：__name__ == __main__，执行内部代码
被其他文件import导入：__name__ == 文件名，不执行内部代码
2.代码逻辑上分层
工具函数、全局变量写在外面，供别人导入使用
程序主逻辑、测试代码写在里面，只在当前文件运行时执行


二、多进程专属作用（Windows重中之重）
Windows创建子进程机制：子进程会重新加载整个.py文件
1.不写if __name__ == '__main__':
主进程创建子进程 → 子进程加载全部代码 → 再次执行创建进程代码
导致无限递归创建子进程 → 程序卡死、报错、CPU飙升
2.写了if __name__ == '__main__':
只有最原始的主进程才会执行创建进程代码
子进程加载文件不会进入该代码块，杜绝递归创建进程，程序正常运行

补充2：put() 方法补充（阻塞/非阻塞）
格式：put(item, block=True, timeout=None)
1. block=True(默认)：队列已满时，代码阻塞等待，直到队列有空位
2. block=False：队列已满，直接抛出异常 queue.Full
3. timeout：设置阻塞超时时间(秒)，超时仍无空间则抛异常

补充3：get() 方法补充（阻塞/非阻塞）
格式：get(block=True, timeout=None)
1. block=True(默认)：队列为空时，代码阻塞等待，直到队列有数据
2. block=False：队列为空，直接抛出异常 queue.Empty
3. timeout：设置阻塞超时时间(秒)，超时仍无数据则抛异常
'''


### 一,队列满阻塞、空阻塞

# 补充：put() / get() 完整参数
# put(item, block=True, timeout=None)
# get(block=True, timeout=None)
# block：控制是否阻塞，默认值为 True
# timeout：阻塞超时时间，单位秒，仅 block=True 时生效

# block = True  【阻塞模式】：原地等待，不报错、不往下执行
# block = False 【非阻塞模式】：不等待，条件不满足直接抛出异常

def queue_block_demo():
    # 创建容量为2的队列，最多存2个元素
    q = Queue(2)
    q.put(111)
    q.put(222)
    print("队列是否已满：", q.full())  # 队列存满，输出 True

    # 队列已满，非阻塞存入
    try:
        q.put(333, block=False)
    except:
        print("队列已满，非阻塞存入失败：队列已满无法添加数据")

    # 取出队列中数据
    print(q.get())   # 取出 111
    print(q.get())   # 取出 222
    print("队列是否为空：", q.empty()) # 队列已空，输出 True

    # 队列已空，非阻塞取出
    try:
        q.get(block=False)
    except:
        print("队列已空，非阻塞取出失败：队列暂无数据")

    # 限时阻塞取值
    try:
        q.get(timeout=2)
    except:
        print("等待2秒仍无数据，超时异常：等待超时未获取到数据")

# 调用函数，执行测试代码
if __name__ == '__main__':
    queue_block_demo()


### 二.进程，队列传参
def write_data(q):
    """写数据子进程：向队列存入数据"""
    for i in range(3):
        q.put(i)
        print(f"子进程写入：{i}")
        time.sleep(0.2)

def read_data(q):
    """读数据子进程：从队列取出数据"""
    while not q.empty():
        data = q.get()
        print(f"子进程读取：{data}")
        time.sleep(0.2)

if __name__ == '__main__':
    # 创建进程队列
    q = Queue()
    # 创建读写子进程
    p_write = Process(target=write_data, args=(q,))
    p_read = Process(target=read_data, args=(q,))

    p_write.start()
    p_write.join()  # 等待写入完成再开始读取
    p_read.start()
    p_read.join()

'''
运行结果：
子进程写入：0
子进程写入：1
子进程写入：2
子进程读取：0
子进程读取：1
子进程读取：2

核心要点：
1. 队列必须作为参数传递给子进程，不能用全局队列（部分系统会失效）
2. 先写后读是常规逻辑，配合join控制执行顺序
3. multiprocessing.Queue 内部自带互斥锁，多进程同时读写不会出现数据错乱
'''


### 三、进程传参 补充易错点
# 前文知识点：args 以元组形式传参
# 高频易错：元组单元素必须加逗号 ,
# 错误写法：args=('小明')  本质是字符串，不是元组，程序报错
# 正确写法：args=('小明',)  单个元素末尾加逗号，才是元组



### 四、守护进程（daemon） 重要知识点
# 1. 含义
# 守护进程：跟随主进程生命周期的子进程
# 规则：
# （1）设置 daemon=True 代表该子进程为守护进程
# （2）主进程代码执行完毕后，直接结束所有守护子进程，不等它执行完
# （3）默认 daemon=False：主进程会等待所有普通子进程执行完毕，程序才结束

# 2. 使用语法：创建进程对象时设置
# p = Process(target=函数, daemon=True)

# 案例1：普通子进程（默认 daemon=False）
def normal_proc():
    time.sleep(2)
    print("普通子进程执行完毕")

# 案例2：守护子进程
def daemon_proc():
    time.sleep(2)
    print("守护子进程执行完毕")

if __name__ == '__main__':
    p1 = Process(target=normal_proc)
    p2 = Process(target=daemon_proc, daemon=True)  # 设置为守护进程

    p1.start()
    p2.start()

    print("主进程执行完毕")

'''
主进程执行完毕
普通子进程执行完毕

运行结果分析：
1. 主进程先打印：主进程执行完毕
2. 守护进程 p2 被直接终止，不会打印内容
3. 普通进程 p1 会继续执行2秒，最后打印：普通子进程执行完毕

使用场景：
1. 后台日志、心跳检测、监控类任务 → 适合做守护进程
2. 必须执行完的业务逻辑 → 不能设置为守护进程

补充规则：
守护进程 内部‘不允许再创建子进程’，否则会抛出异常
'''

# ==============================================
### 五、进程池 Pool（重点！批量创建进程必备）
# 1. 为什么需要进程池？
# 手动创建 Process 适合少量进程；如果任务成千上万，频繁创建/销毁进程会极大消耗系统资源
# 进程池：提前创建指定数量的进程，重复利用，统一管理，提升效率

# 2. 导入 & 基础语法
from multiprocessing import Pool

# 3. 常用方法
# （1）Pool(n) ：创建进程池，n 代表池中最大进程数
# （2）apply() ：同步执行（串行，逐个执行任务，少用）
# （3）apply_async() ：异步执行（并行，任务同时跑，最常用）
# （4）close() ：关闭进程池，不再接收新任务
# （5）join() ：等待进程池所有任务执行完毕

#4.区分串行和并行
#串行：几个人吃饭但是只有一双筷子，A开始吃，然后A吃完B才可以吃
#并行：几个吃饭并且筷子不止一双，有些人是可以同时开始吃饭

#5.理解手动创建和进程池的区别
#（1）手动创建：来一个任务开才创建一个进程，任务结束进程也结束，下一个继续
#（2）进程池：直接用进程池创n个进程，n个进程一起处理多个任务，反复用

#案例 1：手动逐个创建进程（串行执行）
def work(num):
    print(f"任务 {num} 开始执行")
    time.sleep(1)  # 模拟耗时操作
    print(f"任务 {num} 执行完毕")

if __name__ == '__main__':
    start_time = time.time() #获取当前系统时间戳

    # 手动循环创建10个进程，逐个执行
    for i in range(10):
        p = Process(target=work, args=(i,))
        p.start()
        p.join()  # 等待当前进程结束，再执行下一个

    end_time = time.time()
    print(f"手动创建进程(串行)总耗时：{end_time - start_time:.2f} 秒")
#结果是2行同时打印，任务n执行完，任务n+1开始执行，直到结束
# 手动创建进程(串行)总耗时：10.54 秒

#案例 2：手动创建进程（并发执行）
if __name__ == '__main__':
    start_time = time.time()
    process_list = []

    for i in range(10):
        p = Process(target=work, args=(i,))
        p.start()
        process_list.append(p)

    # 最后统一等待所有子进程结束
    for p in process_list:
        p.join()

    end_time = time.time()
    print(f"手动创建进程(并发)总耗时：{end_time - start_time:.2f} 秒")
#结果是10行同时打印出来，0-9任务同时打印，然后又同时打印第二次
# 手动创建进程(并发)总耗时：1.10 秒

#案例 3：进程池（推荐批量任务使用）
if __name__ == '__main__':
    start_time = time.time()

    # 创建进程池：固定3个进程
    pool = Pool(3)

    # 给进程池批量分配10个任务
    for i in range(10):
        pool.apply_async(work, args=(i,))

    # 关闭进程池：不再接收新任务
    pool.close()
    # 等待池中所有任务执行完毕
    pool.join()

    end_time = time.time()
    print(f"进程池总耗时：{end_time - start_time:.2f} 秒")
#结果是3行同时打印，并且任务编号顺序混乱
#进程池总耗时：4.08 秒

'''
1.为何传参都是元组形式
p = Process(target=work, args=(i,))
Process 的 args 形参规定只接收元组类型，所以传参必须写成元组

2.为何进程池的代码打印结果任务编号有些乱？
进程之间互相独立，没有执行先后约定
池里 3 个进程是并行跑的，CPU 不会严格按 0→1→2→3… 的顺序挨个执行
哪个进程先抢到 CPU 时间片，哪个就先打印

3.进程池总结特点：
（1）. 池子最多同时跑n个任务，任务分批执行
（2）. 进程不会重复创建，复用池内进程，性能更高

使用场景：
爬虫、批量文件处理、批量计算等大量重复任务，工作中高频使用

4.apply_async() 异步
(1).把任务丢进进程池 → 主进程不等待，继续往下走
(2).池内多个进程同时并行跑任务
(3).任务顺序由 CPU 调度决定，输出乱序
(4).效率高，是进程池最常用的方式
主进程：发任务 → 发任务 → 发任务...（不等待）
进程池：多个任务同时并行执行

5. apply() 同步（了解即可）
(1).提交一个任务 → 主进程卡住等待任务执行完毕
(2).执行完才会提交下一个任务
(3).全程串行执行，顺序固定、不会乱序
(4).失去进程池并发优势，几乎不用
主进程：发任务 → 等做完 → 再发下一个 → 再等...
进程池：任务逐个执行
'''
