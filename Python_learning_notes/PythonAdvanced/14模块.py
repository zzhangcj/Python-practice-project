###一. os模块

import os
#作用：用于和操作系统进行交互
#1.os.name #指示正在使用的工作平台（返回操作系统类型）
print(os.name) #nt
#对于windows返回nt，对于Linux返回posix

#2. os.geteny(环境变量名) #读取环境变量
# print(os.getenv("path"))

#3. os.path.split() #把目录名和文件名分离，以元组的形式接收，第一个元素是目录路径，第二个元素是文件名
print(os.path.split(r'C:\Users\ASUS\Desktop\简历\简历1.pdf'))
#('C:\\Users\\ASUS\\Desktop\\简历', '简历1.pdf')

#4. os.path.dirname #显示split分割的第一个元素，即目录
print(os.path.dirname(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #C:\Users\ASUS\Desktop\简历
#5. os.path.basename #显示split分割的第二个元素，即文件名
print(os.path.basename(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #简历1.pdf

#注意：如果路径以 / 结尾，则返回空值，如果以 \ 结尾，则报错

#6. os.path.exists() #判断路径（文件或者目录），返回True或者False
print(os.path.exists(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #True
print(os.path.exists(r'C:\Users\ASUS\Desktop\简历\简历2.pdf')) #False
print(os.path.exists(r'C:\Users\ASUS\Desktop\简历')) #True

#7. os.path.isfile() #判断是否存在文件
print(os.path.isfile(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #True
print(os.path.isfile(r'C:\Users\ASUS\Desktop\简历\简历2.pdf')) #False
print(os.path.isfile(r'C:\Users\ASUS\Desktop\简历')) #False

#8. os.path.isdir() #判断是否存在文件夹
print(os.path.isdir(r'C:\Users\ASUS\Desktop\简历\简历1.pdf')) #False
print(os.path.isdir(r'C:\Users\ASUS\Desktop\简历\简历2.pdf')) #False
print(os.path.isdir(r'C:\Users\ASUS\Desktop\简历')) #True

#9. os.path.abspath() #获取当前路径下的绝对路径
print(os.path.abspath("12协程，greenlet，gevent.py"))

#10. os.path.isabs() #判断是否是绝对路径
#C:\Githup_MyFirstRpository\Python-practice-project\Python_learning_notes\PythonAdvanced\12协程，greenlet，gevent.py
print(os.path.isabs(r"C:\Githup_MyFirstRpository\Python-practice-project\Python_learning_notes\PythonAdvanced\12协程，greenlet，gevent.py"))
#True









