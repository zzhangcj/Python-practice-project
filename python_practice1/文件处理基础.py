# import os
# #导入 Python 自带的os 模块，这个模块专门用来操作文件夹、文件、路径，做文件相关操作必须导入它
#
# # 1. 手动让用户输入文件夹路径
# path = input("请输入文件夹路径：")
#
# # 2. 存放所有文件名
# file_list = []
#
# # 3. 遍历、只筛选文件，排除文件夹
# for name in os.listdir(path):
#     #os.listdir() 是函数，产出整体一个列表
#     #这句代码的功能：读取你输入的文件夹，把里面所有东西（文件 + 子文件夹）的名字，全部拿出来
#
#     full_path = os.path.join(path, name)
#     #os.path ,os = 一个大工具箱,os.path = 大工具箱里的 “路径专用小工具箱”
#     #path 专门处理：路径、拼接、判断文件、判断文件夹
#     #小工具箱path里面有个工具叫join()函数，可以拼接路径
#     if os.path.isfile(full_path):
#         #isfile()   函数：判断是不是文件
#         #isdir()    函数：判断是不是文件夹
#         file_list.append(name)
#
# # 4. 打印结果
# print("文件夹下所有文件：")
# for f in file_list:
#     print(f)

# import os
#
# while True:
#     path = input("请输入你要查看的文件夹地址：")
#     if os.path.exists(path):
#         os.path.exists(path)
#         #exists(path)这个路径存在吗？   文件 / 文件夹都可以
#         #isfile(path) 这是一个文件吗？  只能判断【文件】
#         #为什么这里用 exists？因为你输入的是文件夹路径！你要查看文件夹，所以只需要判断：这个文件夹到底存在不存在
#         break
#     else:
#         print("路径输入错误，请重新输入！")
#
# file_list = []
#
# for name in os.listdir(path):
#     # os.listdir() 是函数，产出整体一个列表
#     #这句代码的功能：读取你输入的文件夹，把里面所有东西（文件 + 子文件夹）的名字，全部拿出来
#     full_name = os.path.join(path,name)
#     if os.path.isfile(full_name):
#         file_list.append(name)
#
# print("你要查看的文件夹内有一下文件：")
# for xx in file_list:
#     print(xx)

import os
import shutil
# shutil = 文件操作工具
# 主要功能：复制文件,移动文件,删除文件夹,解压文件

def func1_show_files():
    while True:
        path = input("请输入你要查看的文件夹：")
        if os.path.isfile(path):
            break
        print("输入的路径错误，请重新输入！")
    file_list = []

    for name in os.listdir(path):
        full_name = os.path.join(path,name)
        if os.path.isfile(full_name):
            file_list.append(name)

    print("你要查看的文件夹内的文件如下：")

    for f in file_list:
        print(f)


# 功能2：识别文件后缀（自动分类）
def func2_get_suffix():
    print("\n===== 功能2：识别文件后缀 =====")
    while True:
        path = input("请输入文件夹地址：")
        if os.path.exists(path):
            break
        print("路径错误！")

    # 按后缀分类存放
    suffix_dict = {}
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path):
            # 看看这个东西是文件还是文件夹，我们只处理文件，不处理文件夹
            # 分割文件名和后缀
            suffix = os.path.splitext(name)[-1].lower()
            # os.path.splitext(name)作用：把文件名和后缀切开
            # "photo.jpg" → 切成 ("photo", ".jpg")，[-1]意思：取最后一个元素 → 也就是后缀
            #.lower()：把后缀变成小写
            # 为什么？因为有的文件是.TXT，有的是.txt，程序会认为不一样。统一变小写，程序才能正确分类
            if suffix not in suffix_dict:
                suffix_dict[suffix] = []#注意：这是一个列表

            suffix_dict[suffix].append(name)

    print("\n文件后缀分类结果：")
    for suf, files in suffix_dict.items(): #items () 的作用：遍历字典的一对一对数据
        print(f"\n【{suf}】 类型文件：")
        for f in files:
            print(f"  - {f}")
'''
理解：suffix_dict[suffix] = []#注意：这是一个列表
Python 真正的规则：
规则 1
只要你写：字典 [键名] = 数据
Python 就会自动在字典里创造一个 “键：值”！不管这个键之前有没有！

suffix_dict[".txt"] = []
Python 看到后，心里做了这 3 件事：
看一眼字典里有没有 .txt 这个键→ 没有！
自动创造一个键：".txt"
把右边的空列表，设为这个键的值
'''

# 功能3：自动创建文件夹
def func3_make_folder():
    print("\n===== 功能3：自动创建文件夹 =====")
    base_path = input("请输入要在哪里创建文件夹（路径）：")
    if not os.path.exists(base_path):
        print("路径不存在！")
        return #return 空 = 退出函数，不返回任何值。

    folder_name = input("请输入新文件夹名称：")
    new_folder = os.path.join(base_path, folder_name)

    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
        print(f"✅ 文件夹创建成功：{new_folder}")
    else:
        print("⚠️ 文件夹已存在，无需创建")

# 功能4：移动文件
def func4_move_file():
    print("\n===== 功能4：移动文件 =====")
    source = input("请输入要移动的文件完整路径：")
    target_dir = input("请输入目标文件夹路径：")

    if not os.path.isfile(source):
        print("❌ 源文件不存在")
        return
    if not os.path.exists(target_dir):
        print("❌ 目标文件夹不存在")
        return

    # 移动文件
    shutil.move(source, target_dir)
    print("✅ 文件移动成功！")

# 主菜单
def main():
    while True:
        print("\n================================")
        print("        文件小工具 菜单")
        print("================================")
        print("1 → 查看文件夹内所有文件")
        print("2 → 识别文件后缀（分类）")
        print("3 → 自动创建文件夹")
        print("4 → 移动文件")
        print("0 → 退出程序")
        print("================================")

        choice = input("请输入功能编号：")#choice是变量，存入编号

        if choice == "1":
            func1_show_files()
        elif choice == "2":
            func2_get_suffix()
        elif choice == "3":
            func3_make_folder()
        elif choice == "4":
            func4_move_file()
        elif choice == "0":
            print("程序退出，再见！")
            break
        else:
            print("输入错误，请重新选择！")

if __name__ == "__main__":
    main()

# 这是 Python 标准入口写法。
# 人话翻译：“当我直接运行这个文件时，才执行下面代码”


"""
功能 1：查看文件夹文件 → 必须用 while 循环
因为：用户的目标就是 “查看成功”，不查看成功，这个功能就没意义！
用户输错路径是非常常见的操作,如果输错一次就直接退出功能，用户体验极差

功能 3：创建文件夹 → 不需要 while
因为：创建文件夹的前提是 “父目录必须存在”
比如：你想在 D:\测试 里创建文件夹但 D:\测试 这个目录根本不存在
这时候：你循环 100 次都没用！父目录不存在 → 永远创建失败
用户必须自己先去建好父目录，再来用这个功能。
"""