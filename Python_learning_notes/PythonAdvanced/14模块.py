# ###一. os模块
#
# import os
# #作用：用于和操作系统进行交互
# #1.os.name #指示正在使用的工作平台（返回操作系统类型）
# print(os.name) #nt
# #对于windows返回nt，对于Linux返回posix
#
# #2. os.geteny(环境变量名) #读取环境变量
# # print(os.getenv("path"))
#
# #3. os.path.split() #把目录名和文件名分离，以元组的形式接收，第一个元素是目录路径，第二个元素是文件名
# print(os.path.split(r'C:\Users\ASUS\Desktop\简历\简历1.pdf'))
# #('C:\\Users\\ASUS\\Desktop\\简历', '简历1.pdf')
#
# #4. os.path.dirname #显示split分割的第一个元素，即目录
# print(os.path.dirname(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #C:\Users\ASUS\Desktop\简历
# #5. os.path.basename #显示split分割的第二个元素，即文件名
# print(os.path.basename(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #简历1.pdf
#
# #注意：如果路径以 / 结尾，则返回空值，如果以 \ 结尾，则报错
#
# #6. os.path.exists() #判断路径（文件或者目录），返回True或者False
# print(os.path.exists(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #True
# print(os.path.exists(r'C:\Users\ASUS\Desktop\简历\简历2.pdf')) #False
# print(os.path.exists(r'C:\Users\ASUS\Desktop\简历')) #True
#
# #7. os.path.isfile() #判断是否存在文件
# print(os.path.isfile(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #True
# print(os.path.isfile(r'C:\Users\ASUS\Desktop\简历\简历2.pdf')) #False
# print(os.path.isfile(r'C:\Users\ASUS\Desktop\简历')) #False
#
# #8. os.path.isdir() #判断是否存在文件夹
# print(os.path.isdir(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #False
# print(os.path.isdir(r'C:\Users\ASUS\Desktop\简历\简历2.pdf')) #False
# print(os.path.isdir(r'C:\Users\ASUS\Desktop\简历')) #True
#
# #9. os.path.abspath() #获取当前路径下的绝对路径
# print(os.path.abspath("12协程，greenlet，gevent.py"))
#
# #10. os.path.isabs() #判断是否是绝对路径
# #C:\Githup_MyFirstRpository\Python-practice-project\Python_learning_notes\PythonAdvanced\12协程，greenlet，gevent.py
# print(os.path.isabs(r"C:\Githup_MyFirstRpository\Python-practice-project\Python_learning_notes\PythonAdvanced\12协程，greenlet，gevent.py"))
# #True
#
# # 二.sys模块
# #作用：负责程序和python解释器交互
# import sys
# #1. sys.getdefaultencoding() #获取系统默认编码格式
# print(sys.getdefaultencoding()) #utf-8
# #2. sys.path:获取环境变量路径，跟解释器相关
# print(type(sys.path)) #<class 'list'>
# print(sys.path)
# #以列表的形式返回，第一项为当前所在的工作目录
#
# #3.sys.platform
# #获取操作系统平台名称
# print(sys.platform) #win32
#
# #4. sys.version  #获取python解释器的版本信息
# print(sys.version)
#
#
# ## 三. time模块
# import time
# #三种时间表示
# # 1.时间戳(timetamp)
# # 2.格式化的时间字符串(format time)
# # 3.时间元组(strut_time)
#
#
# #(1).timesleep() #延时操作，以秒为单位
# #获取当前时间时间戳
# #(2). time.time() #以秒计算，从1970年1月1日 00：00：00开始到现在的时间差
# print(time.time())
# print(type(time.time())) #<class 'float'>
#
# #(3)time.localtime()
# #时间戳 --→ 本地struct_time
# print(time.localtime())
# #time.struct_time(tm_year=2026, tm_mon=7, tm_mday=11, tm_hour=9, tm_min=0, tm_sec=14, tm_wday=5, tm_yday=192, tm_isdst=0)
# print(type(time.localtime())) #<class 'time.struct_time'>
# #这是一个时间元组
#
# t = time.localtime()
# print(t.tm_year) #2026
#
# #时间元组struct.time --→ 固定格式字符串
# #(4)time.asctime()
# print(time.asctime()) #Sat Jul 11 09:06:39 2026
#
# #把struct.time换成固定的字符串表达式
# print(time.asctime(t)) #Sat Jul 11 09:06:39 2026
#
# #时间戳 --→ 固定格式字符串
# #(5)time.ctime(时间戳)
# t1 = time.time()
# print("t1:",time.ctime(t1))
# #t1: Sat Jul 11 10:06:33 2026
#
# #时间元组struct.time --→ 自定义格式字符串
# #(6).time.strftime(格式化字符串,struct.time)
# print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
# #2026-07-11 10:06:33
# t2 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
# print(type(t2)) #<class 'str'>
#
# #时间字符串 --→ 时间元组struct.time
# #(7).time.strptime(时间字符串，格式化字符串)
# print(time.strptime("2026-07-11","%Y-%m-%d"))
# #time.struct_time(tm_year=2026, tm_mon=7, tm_mday=11, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=5, tm_yday=192, tm_isdst=-1)
#
# t3 = time.strptime("2026-07-11","%Y-%m-%d")
# print(type(t3))
# #<class 'time.struct_time'>

## 四.logging模块
#1.作用：用于记录日志信息
#2.日志的作用：
#   程序调试
#   了解软件程序运行情况是否正常
#   软件程序运行故障分析与问题定位
#
# #3.级别排序
# #CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
# import logging
# # logging.debug("我是debug")
# # logging.info("我是info")
# # logging.warning("我是warning") #WARNING:root:我是warning
# # logging.error("我是error") #ERROR:root:我是error
# # logging.critical("我是critical") #CRITICAL:root:我是critical
#
# #logging默认的level就warning，也就是说，logging只会显示级别大于warning的日志信息
#
# #4.logging.basicCongfig() #配置root logger的参数
# #  （1）filename:指定日志文件的文件名，所有会显示的日志都会存放到这个文件中去
# logging.basicConfig(filename='log.log')
# logging.debug("debug")
# logging.info("info")
# logging.warning("warning")
# logging.error("error")
# logging.critical("critical")
# #  （2）filemode:文件的打开方式，默认是a，追加模式
# #   logging.basicConfig(filename='log.log',filemode='a')
# #  （3）level:指定日志显示级别，默认是警告信息warning
# #   logging.basicConfig(filename='log.log',filemode='w',level=logging.NOTSET)
# #   这里所有信息都能显示，包括debug，info
# #   （4）format:指定日志信息的输出格式
# #   logging.basicConfig(filename='log.log',filemode='w',level=logging.NOTSET,format='%(levelname)s:%(asctime)s\t%(message)s')


## 五.random模块
#作用：用于实现各种分布的伪随机数生成器，可以根据不同实数分布来随机生成值
import random
#1.random.random() 产生大于0且小于1之间的小数
print(random.random()) #每一次打印结果都不一样

#2. random.uniform() #产生指定范围的随机小数
print(random.uniform(1,3))

#3.random.randint() #产生指定范围内的随机整数，包括开头结尾，即闭区间
print(random.randint(1,3))

#4. random.randrange(start,stop,[step]) #产生[start,stop)范围内的整数
#step 指定产生随机的步长，随机选择一个数据
print(random.randrange(2,5,2)) #结果在2和4两个数之间变化
















