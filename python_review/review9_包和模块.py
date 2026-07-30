"""一、概念简答题"""

# import module 和 from module import func 两种导入方式有什么核心区别？
'''
import module：导入整个模块，使用时需要 模块名.函数名 的方式调用
from module import func：只导入模块中的指定函数 / 变量，可直接使用函数名调用
'''

# 解释 if __name__ == '__main__': 的作用和原理，这段代码在什么情况下会执行？
'''
1.区分运行身份
Python 每个脚本自带__name__内置变量
直接运行当前文件：__name__ == __main__，执行if 里面代码
被其他文件import导入：__name__ == 文件名，不执行if 里面代码
2.作用
可以用在本文件内用这样的测试代码来测试函数
防止本文件的测试代码，在被别人 import 的时候意外执行，干扰别人程序
'''
# Python 虚拟环境 venv 的作用是什么？为什么企业项目推荐使用虚拟环境？
'''
是什么？
虚拟环境 venv，用来给每个项目创建独立 Python 环境，各个项目第三方包互相隔离，解决包版本冲突

什么时候用？
一台电脑同时做好几个不同项目，不同项目需要同一个库的不同版本

理解关键
（1）不同虚拟环境，安装的第三方包互不干扰。
（2）激活虚拟环境之后 pip 安装的包，只属于当前这个虚拟环境，不会跑到全局。
'''

# 列出 3 个 pip 常用命令及对应功能（安装、卸载、查看已安装包）
'''
安装包：pip install 包名
卸载包：pip uninstall 包名
查看已安装包：pip list
'''


"""二、代码运行结果题"""
# a.py
print("模块a被加载")
def test():
    print("执行a.test函数")
# 模块a被加载
# a文件直接运行
# 执行a.test函数

if __name__ == '__main__':
    print("a文件直接运行")
    test()

# b.py

import a
print("模块b被加载")
a.test()
# 模块a被加载
# 模块b被加载
# 执行a.test函数

"""三、实操简答题"""
# 如何创建一个名为 venv 的 Python 虚拟环境？分别写出 Windows 系统和 Linux/Mac 系统下的激活命令
r'''
创建虚拟环境：python -m venv venv
激活命令：
Windows：venv\Scripts\activate
Linux/Mac：source venv/bin/activate
'''