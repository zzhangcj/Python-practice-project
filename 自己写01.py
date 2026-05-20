import os
import shutil
from time import strftime
import datetime
import subprocess


# shutil = 文件操作工具
# 主要功能：复制文件,移动文件,删除文件夹,解压文件

def func1_show_files():
    print("\n===== 功能1：查看文件夹内所有文件 =====")
    while True:
        path = input("请输入你要查看的文件夹：")
        if os.path.isdir(path):
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

def func2_get_suffix():
    print("\n===== 功能2：识别文件后缀 =====")
    while True:
        path = input("请输入文件地址：")
        if os.path.exists(path):
            break
        print("路径输入错误！")

    suffix_dict = {}
    for name in os.listdir(path):
        full_path = os.path.join(path,name)
        if os.path.isfile(full_path):
            suffix = os.path.splitext(name)[-1].lower()
            if suffix not in suffix_dict:
                suffix_dict[suffix] = []
            suffix_dict[suffix].append(name)

    print("\n文件后缀分类结果：")
    for suf,files in suffix_dict.items():
        print(f"\n【{suf}】类型文件：")
        for f in files:
            print(f)
'''
.items() 到底是什么
解释：字典默认只能遍历 “键”, .items() 让你能同时拿到 键 + 值
suffix_dict = {
    "txt": ["a.txt", "b.txt"],
    "jpg": ["1.jpg", "2.jpg"]  }
    
items() 会让他变成元组：
("txt", ["a.txt", "b.txt"])
("jpg", ["1.jpg", "2.jpg"])
'''

def func3_make_folder():
    print("\n===== 功能3：自动创建文件夹 =====")
    path = input("请输入你要在那里创建文件夹（路径）：")
    if not os.path.exists(path):
        print("路径不存在！")
        return

    folder_path = input("请输入新的文件夹名称：")
    new_folder = os.path.join(path,folder_path)

    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
        print(f"✅ 文件夹创建成功：{new_folder}")
    else:
        print("⚠️ 文件夹已存在，无需创建")

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


#功能5：复制文件
def func5_copy_file():
    print("\n===== 功能5：复制文件 =====")
    source = input("请输入要复制的文件完整路径：")
    target_dir = input("请输入目标文件夹路径：")

    if not os.path.isfile(source):
        print("❌ 源文件不存在")
        return

    if not os.path.exists(target_dir):
        print("❌ 目标文件夹不存在")
        return

    shutil.copy(source, target_dir)
    print("✅ 文件复制成功！")

#功能6：删除文件
def func6_delete_file():
    print("\n===== 功能6：删除文件 =====")
    file_path = input("请输入要删除的文件完整路径：")

    if not os.path.isfile(file_path):
        print("❌ 文件不存在")
        return

    confirm = input("确定要删除吗？(y/n):")
    if confirm.lower() == "y":
        os.remove(file_path)
        print("✅ 文件删除成功！")
    else:
        print("❌ 文件删除取消！")

#功能7:删除文件夹
def func7_delete_folder():
    print("\n===== 功能7：删除文件夹 =====")
    folder_path = input("请输入要删除的文件夹完整路径：")

    if not os.path.isdir(folder_path):
        print("❌ 文件夹不存在")
        return
    
    confirm = input("确定要删除文件夹（包含里面所有文件）吗？(y/n):")
    if confirm.lower() == "y":
        shutil.rmtree(folder_path)
        print("✅ 文件夹删除成功！")
    else:
        print("❌ 文件夹删除取消！")

#功能8：文件重命名
def func8_rename_file():
    print("\n===== 功能8：文件重命名 =====")
    file_path = input("请输入要重命名的文件完整路径：").strip().strip('"').strip("'")
    #.strip().strip('"').strip("'"),去掉空格,去掉用户复制时带的双引号,单引号,让路径干净完整
    file_path = os.path.normpath(file_path)
    #normpath()函数：将文件路径标准化，解决路径中的..和.(去除多余的点点，斜杠，并且解决转义字符的影响)
    if not os.path.isfile(file_path):
        print("❌ 文件不存在")
        return
    new_name = input("请输入新的文件名（包含后缀）：")
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    print("✅ 文件重命名成功！")

#功能9：日志输出
def func9_log_output():
    print("\n===== 功能9：日志输出 =====")
    #获取要记录的日志内容
    log_content = input("请输入要输出的日志内容：")
    if not log_content:
        print("❌ 日志内容不能为空")
        return
    #日志存放路径
    log_path = "file_tool_log.txt"

    #获取当前日期和时间
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{current_time}] {log_content}\n"

    with open(log_path, "a") as f:
        f.write(log_line)
        print(f"✅ 日志已经保存！文件路径：{os.path.abspath(log_path)}")
        print("日志内容预览：",log_line.strip())

#功能10：文件搜索
def func10_file_search():
    print("\n===== 功能10：文件搜索 =====")
    
    while True:
        search_path = input("请输入要搜索的文件夹路径：").strip().strip('"').strip("'")
        search_path = os.path.normpath(search_path)
        if os.path.isdir(search_path):
            break
        print("输入的路径错误，请重新输入！")
    #获取搜索关键字
    keyword = input("请输入要搜索的文件名关键字：").strip()

    #是否递归子文件夹
    recursive = input("是否递归子文件夹？(y/n):").lower()
    recursive = recursive != 'n' 
    #如果输入的是n，则不递归子文件夹,输入其他的都要递归，返回True
    #可以理解为需要需要的结果大多为True，少数为False


    #是否区分大小写
    case_sensitive = input("是否区分大小写？(y/n):").lower()
    case_sensitive = (case_sensitive == "y") 
    #如果输入的是y，则区分大小写,输入其他的都不区分,返回False
    #可以理解为需要需要的结果大多为False，少数为True

    print(f"正在搜索：{search_path} 关键字：{keyword}，递归：{recursive}，区分大小写：{case_sensitive}.....")
    result_files = []

    def search_in_dir(dir_path):
        try:
            for name in os.listdir(dir_path):
                full_path = os.path.join(dir_path, name)

                if os.path.isfile(full_path):
                    if keyword: #等价于 if keyword != "":
                        # 如果用户输入了关键词 → 执行下面的if语句，进行匹配
                        # 如果用户什么都没输 → 跳到下面最后一个else，直接显示所有文件
                        if case_sensitive:
                            if keyword in name:
                                result_files.append(full_path)
                            else:
                                if keyword.lower() in name.lower():
                                    result_files.append(full_path)
                                #这里不需要else的原因：符合条件则收入列表，不符合则下一个
                    else:
                        #如果没有关键字，则直接添加
                        result_files.append(full_path)
                    
                elif os.path.isdir(full_path) and recursive:
                    #如果文件是文件夹，并且需要递归，则递归搜索
                    search_in_dir(full_path)
        except PermissionError:
            pass
        except Exception as e:
            print(f'访问{dir_path}时出错：{e}')

    #开始搜索
    search_in_dir(search_path)


    '''
    在 if 判断里：
    下面这些情况 → 自动当成 False
    空字符串 "",空列表 [],空字典 {},数字0, None

    下面这些情况 → 自动当成 True
    有内容的字符串 "abc"
    有内容的列表 [1,2,3]
    非 0 数字
    '''
    #显示结果
    if result_files:#等价于：if len(result_files) > 0:
        #如果列表里有内容（不是空列表）→ 条件成立,和上面if keyword一样的
        print(f"\n✅ 找到{len(result_files)}个文件：")
        print("=" * 60)
        for i,file_path in enumerate(result_files,1):#enumerate(...,1)：给文件从 1 开始顺序编号
            file_size = os.path.getsize(file_path)
            size_str = format_file_size(file_size)
            print(f"{i:3d}. {file_path}({size_str})")

        '''
        1.为什么这一段额外选项的缩进和 for 循环齐平？
        是因为：它属于 “显示完所有文件之后” 才执行的代码，不属于 for 循环内部
        
        2.enumerate 返回一堆元组
        (0, 文件1)
        (1, 文件2)
        (2, 文件3)
        于是能用for后面加两个参数i和file_path来遍历
        
        3.{i:3d} 是什么？
        d = 整数（digit）, 3 = 占 3 个字符宽度, 合起来：把数字 i 右对齐，占 3 个位置，不够用空格补齐
        为了让显示更为整齐
        不去右对齐：
        1   → 右对齐，占3格
         2  → 右对齐，占3格
        10  → 右对齐，占3格
        100 → 占3格
        
        右对齐之后：
         1. 文件xxx
         2. 文件xxx
        10. 文件xxx
        11. 文件xxx
        '''

        # 提供额外选项
        print("\n" + "=" * 60)
        print("额外选项：")
        print("1 → 导出搜索结果到日志")
        print("2 → 复制某个文件路径到剪贴板")
        print("0 → 返回主菜单")

        sub_choice = input("请选择（直接回车返回主菜单）：").strip()

        if sub_choice == "1":
            #导出日志
            export_search_result_to_log(result_files, search_path, keyword)
        elif sub_choice == "2":
            try:
                idx = int(input(f"请输入要复制的文件编号（1-{len(result_files)}）："))
                if 1 <= idx <= len(result_files):
                    copy_to_clipboard(result_files[idx-1])
                    print("✅ 路径已复制到剪贴板")
                else:
                    print("❌ 编号无效")
            except ValueError:
                print("❌ 输入无效")

    else: #这个else对应最上面的”显示结果"哪里的if
        print(f"\n❌ 未找到匹配的文件（关键词：{keyword if keyword else '无'}）")

'''
1.{keyword if keyword else '无'}
 Python 三元表达式（一行写完 if else）
语法： 结果A if 条件 else 结果B
原句的翻译：
如果 keyword 不为空（用户输入了东西）→ 显示 keyword
否则 → 显示 “无”

2.为什么这个自定义函数放能放这么后面？
函数定义的顺序无所谓,只要调用时，函数已经存在即可！
简单比喻：
先写 “主角要吃饭”, 提出需求
再写 “做饭的方法”, 解决问题
'''

# 辅助函数：格式化文件大小
def format_file_size(size_bytes):
    #将字节转换为可读格式
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}" #.1f = 保留 1 位小数
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"

# 辅助函数：导出搜索结果到日志
def export_search_result_to_log(result_files, search_path, keyword):
    #将搜索结果导出到日志文件

    log_path = "search_results_log.txt"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 60}\n")
        f.write(f"搜索时间：{current_time}\n")
        f.write(f"搜索路径：{search_path}\n")
        f.write(f"搜索关键词：{keyword if keyword else '无'}\n")
        f.write(f"找到文件数：{len(result_files)}\n")
        f.write(f"{'=' * 60}\n")
        for file_path in result_files:
            file_size = os.path.getsize(file_path)
            size_str = format_file_size(file_size)
            f.write(f"{file_path}({size_str})\n")
        f.write(f"{'=' * 60}\n")

    print(f"✅ 搜索结果已导出到：{os.path.abspath(log_path)}")
    '''
    log_path = "search_results_log.txt"
    这叫相对路径,意思是：在程序当前运行的文件夹里，创建这个文件
    
    os.path.abspath(路径) 做了 3 件事：
    获取当前程序运行的文件夹
    把你给的文件名拼到后面
    返回完整路径字符串
    '''

# 辅助函数：复制到剪贴板（跨平台）
def copy_to_clipboard(text):
    try:
        subprocess.run(['clip'],input=text.strip().encode('gbk'),check = True)
    except Exception as e:
        print(f"⚠️ 复制失败：{e}")

'''
1.subprocess.run () = 让 Python 调用系统命令（CMD 命令）
你 Windows 里手动打开 CMD，输入：
echo 文本 | clip
就能把文字复制到剪贴板。
subprocess.run 就是让 Python 帮你自动执行这条 CMD 命令

2.['clip']
运行 Windows 自带剪贴板工具 clip.exe

3.input=文本
把要复制的文字传给 clip 工具

4.encode('gbk')
Windows 中文系统必须用 GBK 编码，否则复制中文会乱码

5.check=True = 运行出错就抛出异常
如果命令执行失败（比如 clip 命令坏了）
不加 check=True → 默默失败
加了 check=True → 直接报错，进入 except 提示 “复制失败”
作用：让程序知道 “命令有没有成功执行”，方便报错提示用户。
'''


#功能11: 文件压缩
#功能12：文件解压
    





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
        print("5 → 复制文件")
        print("6 → 删除文件")
        print("7 → 删除文件夹")
        print("8 → 文件重命名")
        print("9 → 日志输出")
        print("10 → 文件搜索")
        print("0 → 退出程序")
        print("================================")

        choice = input("请输入功能编号：")

        if choice == "1":
            func1_show_files()
        elif choice == "2":
            func2_get_suffix()
        elif choice == "3":
            func3_make_folder()
        elif choice == "4":
            func4_move_file()
        elif choice == "5":
            func5_copy_file()
        elif choice == "6":
            func6_delete_file()
        elif choice == "7":
            func7_delete_folder()
        elif choice == "8":
            func8_rename_file()
        elif choice == "9":
            func9_log_output()
        elif choice == "10":
            func10_file_search()
        elif choice == "0":
            print("程序退出，再见！")
            break
        else:
            print("输入错误，请重新选择！")

if __name__ == "__main__":
    main()
