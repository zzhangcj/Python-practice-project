""""""
from os import write

"""
一、基础概念题
(1)简述 Python 中open()函数常用的文件打开模式（至少写出 r、w、a、rb、wb 5 种）的含义与区别。
r ： 只读
w ： 只写 （文件存在则清空原内容覆盖写入，不存在则自动创建）
a ： 追加模式 （文件存在则在末尾追加内容，不存在则自动创建）
rb: 二进制只读模式 （用于读取文件，视频，压缩包等非文本文件）
wb: 二进制只写模式 （用于写入二进制文件）

(2)为什么强烈推荐使用with open()操作文件，而不是open()+close()的写法？
with open 进入代码块自动打开文件，退出时无论是否发生异常，都会自动调用close()关闭文件
手动open()+close() 当中间代码报错，close()不会执行，会造成资源泄露

(3)分别说明read()、readline()、readlines()三个方法的作用、返回值类型，以及适用场景。
read()          一次性读取文件全部内容                返回字符串    文件体积小、需要完整处理全文的场景
readline()      一次读取一行内容，指针下移一行          返回字符串    大文件逐行处理、只需读取前几行的场景
readlines()     一次性读取所有行，每行作为一个元素       返回列表      需要按行遍历、快速获取所有行内容的场景

(4)文件打开模式中，w和a的核心区别是什么？二者打开不存在的文件时分别会发生什么？
w：覆盖写入，打开已有文件会直接清空原内容
a：追加写入，打开已有文件会在内容末尾续写，保留原内容
-->二者打开不存在的文件时，都会自动创建新文件，不会报错
"""

"""
二、代码结果题
已知文本文件test.txt的内容如下（共 3 行，第三行为空行）：
hello world
python
"""

#1.
f = open("test.txt", "r", encoding="utf-8")
res = f.read()
print("\n",type(res), res)
f.close()
# <class 'str'> hello world
# python

#2.
f = open("test.txt", "r", encoding="utf-8")
res1 = f.readline()
res2 = f.readline()
res3 = f.readline()
print("\n",res1, res2, res3)
f.close()
# hello world
# python

#3.
f = open("test.txt", "r", encoding="utf-8")
res = f.readlines()
print("\n",type(res), res)
f.close()
# <class 'list'>['hello world\n', 'python']

"""三、编程实操题"""
# 1、基础读写：使用with open语法，向demo.txt写入 3 行文本：第一行\n第二行\n第三行，再读取全部内容打印
with open("demo.txt","w",encoding="utf-8") as f:
    f.write("第一行\n第二行\n第三行")
# 2、JSON 操作：
# （1）简述json.dumps()和json.dump()、json.loads()和json.load()的区别。
'''
    函数	                          作用	              操作对象
json.dumps(obj)	        Python 对象 → JSON 字符串	    字符串（内存）
json.loads(json_str)	JSON 字符串 → Python 对象	    字符串（内存）
json.dump(obj, fp)  	Python 对象 → 直接写入文件	    文件对象 fp
json.load(fp)	        读取文件 JSON → Python 对象	文件对象 fp
记忆点
✅ s = string，带 s 就是和字符串打交道；不带 s 就是和文件打交道
'''



# （2）编写代码：将字典user = {"name":"张三", "age":20, "hobby":["coding","reading"]}写入user.json文件；
# 再读取该文件，将 age 修改为 21 后重新写入文件。
import json
user = {"name":"张三", "age":20, "hobby":["coding","reading"]}
# 写入json文件
with open("user.json","w",encoding="utf-8") as f:
    json.dump(user,f,ensure_ascii=False,indent=2)

# 读取并修改
with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    data["age"] = 21

# 重新写入
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)



"""
知识补充：
1. ensure_ascii 👉 处理中文 json 必备参数！
默认 ensure_ascii=True
中文会被转义：{"name":"\u5f20\u4e09"}

ensure_ascii=False -->中文正常显示 {"name":"张三"}


2. indent=2  --> 控制格式化缩进
#indent=None（默认）：输出紧凑一行
{"name":"张三","age":20}

#indent=2：自动换行、缩进排版，人方便阅读
{
  "name": "张三",
  "age": 20
}

3.读取并修改 --> 这里的”r“表示只读，为什么能修改内容呢
with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f) #把磁盘文件内容读到内存，变成字典
    data["age"] = 21 # ✅ 修改【内存中的字典】，和磁盘文件无关！
    
r 模式只是限制：不能直接往文件里写东西！
你修改的变量 data，是读到内存里的字典副本，根本不是直接操作磁盘上的文件
因此，修改后还要 重新写入
"""
# 3、CSV 操作：编写代码，向student.csv写入表头（姓名,年龄,专业）和两行数据（张三,20,计算机、李四,21,物联网）；
# 再读取整个 CSV 的内容，逐行打印
import csv

#写入CSV
with open("student.csv","w",encoding="utf-8",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["姓名", "年龄", "专业"])
    writer.writerow(["张三", 20, "计算机"])
    writer.writerow(["李四", 21, "物联网"])

#读取CSV
with open("student.csv","r",encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

"""
1. newline="" 重中之重（csv 专属坑）
Windows 系统下，如果不写 newline=""，用 csv 模块写入文件，每行之间会多出一行空白行。
newline="" 告诉 Python：不要自动转换换行符，交给 csv 库自行处理换行。
只要使用 csv.writer 写入文件，强制加上 newline=""，这是固定规范。

2. csv.writer(f)

3. writerow(列表)
writerow(row)：写入一行，参数必须是列表 / 元组,列表内每一个元素，代表表格里的一列单元格

writerow() → 单行
writerows(嵌套列表) → 一次性写入多行

rows = [
    ["姓名","年龄"],
    ["张三",20]
]
writer.writerows(rows)

5、csv.reader(f)：读取 csv，循环迭代，每一行自动解析成列表

6.复习文件操作，为什么同时学 JSON、CSV？各自是干嘛的？
文件操作 = 把内存中的数据，持久保存到硬盘；或者把硬盘数据读到内存

但是纯文本 f.write() 只能写字符串
-->复杂数据（字典、表格）直接写入文件会很麻烦，于是诞生了两种标准化格式

(1)JSON 适合字典、嵌套结构、对象数据
一条一条独立的结构化数据（用户信息、参数配置）；
支持嵌套 {"name":"张三","hobby":["看书","打球"]}
特点：树形嵌套结构，键值对为主。
短板：不适合大量表格形式数据

(2)CSV 适合二维表格数据（Excel 表格）
典型场景： 学生名单、商品清单、测试报表；
每行一条记录，固定表头，没有复杂嵌套。
可以直接用 Excel/WPS 打开查看、编辑。
特点：扁平表格，一行 = 一条数据，一列 = 一个字段。
短板：不支持多层嵌套结构。

(3)总结：
如果你要保存一个用户信息（姓名、年龄、爱好列表） → 用 JSON
如果你要保存几十个学生的清单（像 Excel 表格） → 用 CSV
"""


