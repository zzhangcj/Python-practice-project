# # ###1.异常
# # #定义：是一个事件，这个事件在程序执行过程中发生，影响了程序的正常执行
# print('a')
# # """
# # print(a)
# # NameError: name 'a' is not defined
# # 这里算一个异常
# #
# # 当Python检测到错误，解释器无法继续执行，出现报错
# # 这就是‘异常’，感觉就是报错
# #
# # 所以这一章就是如何处理异常，报错
# # """
# #
# # ##2.抛出异常 raise
# # #步骤：
# # #1.创建一个Exception('xxx')对象，xxx---异常提示信息
# # #2.raise Exception("冰冰抛出了一个异常“)
# # def funa():
# #     print("嘻嘻嘻，笑死我了")
# #     raise Exception("冰冰抛出了一个异常")
# #     print("哈哈哈，笑死我了") #执行了raise语法，代码就不会继续往下运行
# # funa()
# # """
# # 嘻嘻嘻，笑死我了 #这里正常输出
# # Exception: 冰冰抛出了一个异常 #这里是红字
# # 后面的“哈哈哈“没有执行，原因看上面黄色波浪线
# # """
# #
# # ##3.需求：密码长度不够，报出异常
# # #分析：用户输入密码，判断输入的长度，不足6位，就报错
# # # 即抛出自定义异常，并捕获该异常
# #
# # def login():
# #     pwd = input("请输入密码：")
# #     if len(pwd) >= 6:
# #         return "密码输入成功"
# #     raise Exception("密码长度不足六位，输入失败")
# # print(login())
# # '''
# # 请输入密码：123
# # Exception: 密码长度不足六位，输入失败
# #
# # 为啥不用else：因为如果return了函数就结束了，不return就继续执行，跟else效果是一致的
# # '''
# #
# # #由于出现异常，后续代码无法执行，则需要捕获异常
# # try:
# #     print(login())
# # except Exception as e:
# #     print(e)
# # print(1232)
# # """
# # 请输入密码：213
# # 密码长度不足六位，输入失败
# # 1232
# #
# # 注意这里要运行，得注释掉print(login())
# #
# # 总结：捕获异常是为了检测到异常时，代码还能继续运行下去，程序还能执行
# # """
# #
#
#
#
#
#
# ###1.模块
# #含义：一个py文件就是一个模块，导入一个模块本质上就是执行一个py文件
# #
# ##2.分类
# # 2.1 内置模块
# # 比如：random、time、os、logging...直接导入即可使用
# #
# # 2.2 第三方模块（第三方库）
# # 下载：cmd 窗口输入pip install模块名
# # 可以尝试在cmd窗口
# # pip install pygame
# # pip list
# # pip uninstall pygame
#
# #2.3 自定义模块
# #即自己在项目中定义的模块
# """
# 意思是说不要起一些名称与内置的那些py文件相同的名
# 如果与内置的那些py包冲突会导致运行不了
# 就相当于命名一样，变量名如果写成print那样会冲突
# """
#
# ###2.导入模块
# #2.1 方法一：import
# #语法：import 模块名
# #调用功能：模块名.功能名
# import pytest15_1
# #调用pytest15_1中的name变量
# print(pytest15_1.name)
# # 这是pytest模块
# # zcj
#
# #调用pytest模块中的funa()
# pytest15_1.funa() #这里是pytest模块中的funa()
#
# 注意可以一个import导入多个模块，但最好是一个模块单独一个import
#
# #2.2 方法二：from...import...
# #从模块中调用指定部分
# #语法：from 模块名 import 功能1,功能2
#
# from pytest15_1 import funa
# #导入函数只需要函数名，不需要小括号()
# funa() #这里是pytest模块中的funa()
# #调用功能的时候，直接输入功能即可，不用添加模块名
# #就是不用写pytest15_1.funa(), 直接用funa()
#
# '''
# funb()
# NameError: name 'funb' is not defined. Did you mean: 'funa'?
# 没有导入funb，直接用就会报错
# '''
#
# #2.3 方法三：from ... import *
# from pytest15_1 import *
# #把模块中的所有内容都全部导入 *表示全部
# funa() #这里是pytest模块中的funa()
# print(name) #zcj
#
# '''
# 不建议过多使用from...import...声明。有时候命名冲突会造成一些错误
# from pytest15_1 import *
# from pytest15_2 import *
# #这里假如pytest15_2的内容和pytest15_1相同，只是print内不同
# 那么最后在这里funa()或者同名的一切以pytest15_2为准
# '''






# ##3 as起别名
# # 语法：import 模块名 as 别名
# #3.1 给模块起别名
# import pytest15_1 as pt
# #调用模块中的funa,打印name
# print(pt.name) #zcj
# pt.funa() #这里是pytest模块中的funa()
#
# #3.2 as给功能起别名
# #语法：from 模块名 import 功能 as 别名
# from pytest15_1 import funa as fa,name,funb as fb
# fa() #这里是pytest模块中的funa()
# print(name) #zcj
# fb() #这是pytest中的funb()
#
# 注意：导入多个功能，使用逗号, 将功能与功能隔开，后面的同样可以起别名
#
# ##4. 内置全局变量_name_
# #语法：if __name__ =="__main__"
# #作用：用来控制py文件在不同的应用场景执行不同的逻辑
#
# #4.1 _name_
# #（1）文件在当前程序执行（即自己执行自己）：__name__ =="__main__"
# #if __name__ == "__main__" 就是：只有自己运行时才执行的代码
#
# #（2）文件被当作模块被其他文件导入：__name__ == 模块名
# #被当作模块导入时，下面的代码不会显示出来
#
# import pytest15_2 as p2
# p2.test()
# #这是pytest2会显示的内容
# #哈哈哈
#
# """
# 这个东西到底有什么用？
# 防止导入模块时，把模块里的测试代码也跑出来！
# """




###4.包 Python Package
#4.1 含义：就是项目结构中的文件夹/目录
#4.2 与普通文件夹的区别：包是含有_init_.py的文件夹
#4.3 作用：将有联系的模块放到同一个文件夹下，能有效避免模块名称冲突问题，让结构清晰
#列如两个包里有一个相同命名的模块，可以通过包名来区分它们
#4.4 新建包：new -> python package

#4.5 import导入包的时候，首先执行_init_.py的文件的代码
#4.5.1 导包方式一

import pack_01 #这里是_init_.py

"""
init文件须知
#注意：不建议在init中写大量代码，尽量保证init文件内容简单
#主要作用：导入这个包内的其他模块
"""

# #4.5.2 导包方式二

from pack_01 import Register
Register.reg() #这里是Register函数

##5.__all__
#含义：本质上是一个列表，列表里的元素就代表要导入的模块
#作用：可以控制引入的东西
"""
_init_.py中的代码如下
__all__ = ['Register','login'] #相当于导入[]中定义的模块

"""
from pack_01 import *
#  * 表示全部/所有
Register.reg() #这里是Register函数
login.log() #这是一个登录函数

##6.包的本质依然是模块，包也可以包含包，
#在某个包目录下，依然可以创建包






















