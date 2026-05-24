##1.with open
#作用：代码执行完，系统会自动调用f.close()，可以省略文件关闭步骤
with open('test.text','w') as f:#f是文件对象
    f.write('emmmm....')
print(f.closed) #True
#这个可以用来省略f.close()

###一，编码格式
#1.encoding
with open('bianma.text','w',encoding = 'utf-8') as h:
    h.write("冰冰18岁") #不写encoding会出现乱码,

with open('bianma.text',encoding = 'utf-8') as h:
    print(h.read()) #不写encoding会报错，windows默认gbk，这里要改为utf-8

#2.案例：图片复制 'rb'
"""
1.读取图片
图片是一个二进制文件，想要写入必须先拿到

2.写入图片
"""
with open(r"C:\Users\ASUS\Pictures\Camera Roll\屏幕截图测试.png",'rb') as file:
    img = file.read()
    print(img)

# 将读取到的内容写入到当前文件中
with open(r'C:\python学习\屏幕截图测试.png','wb') as g:
    g.write(img)
'''
r = read（读）
w = write（写）
b = binary（二进制）
✅ 'rb' = read binary（以二进制模式读取）
✅ 'wb' = write binary（以二进制模式写入）
'''

#3.目录常用操作 os模块
#1).文件重命名 os.rename(旧名字,新名字)
import os
os.rename('test.text','bingbing.txt')

#2)删除文件 os.remove()
os.remove(r'C:\python学习\屏幕截图测试.png')

#3)创建文件夹 os.mkdir()
#4)删除文件夹 os.rmdir()
#5)获取当前目录 os.getcwd()
print(os.getcwd()) #C:\python学习\PythonAdvanced

#6)获取目录列表 os.listdir() #以列表的形式
print(os.listdir()) #获取当前目录列表
print(os.listdir('../')) #获取上一级目录的列表
print(type(os.listdir())) #<class 'list'>