import os
import shutil
from email.policy import default
from time import strftime
import datetime
import subprocess
import zipfile

from pandas.core.tools.datetimes import should_cache


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


#这里移动文件的代码依旧有优化空间：比如选择移动单个文件，路径输入却是文件夹，没有报错说是文件夹或者重新选
def func4_move_file():
    print("\n===== 功能4：移动文件/文件夹 =====")

    # 选择移动类型
    print("移动类型：")
    print("1 → 移动单个文件")
    print("2 → 移动文件夹")
    print("3 → 批量移动文件（按后缀）")
    move_type = input("请选择（1/2/3）：").strip()

    if move_type == "1":
        # 移动单个文件
        while True:
            source = input("请输入要移动的文件完整路径：").strip().strip('"').strip("'")
            source = os.path.normpath(source)
            if os.path.isfile(source):
                break
            print("❌ 源文件不存在，请重新输入！")

        while True:
            target_dir = input("请输入目标文件夹路径：").strip().strip('"').strip("'")
            target_dir = os.path.normpath(target_dir)
            if os.path.exists(target_dir):
                break
            print("❌ 目标文件夹不存在，请重新输入！")

        # 处理目标路径中的同名文件
        target_path = os.path.join(target_dir, os.path.basename(source))
        target_path = handle_duplicate_file(target_path)

        try:
            shutil.move(source, target_path)
            print(f"✅ 文件移动成功！")
            print(f"📂 从：{source}")
            print(f"📂 到：{target_path}")


        except Exception as e:
            print(f"❌ 移动失败：{e}")

    elif move_type == "2":
        # 移动文件夹
        while True:
            source = input("请输入要移动的文件夹完整路径：").strip().strip('"').strip("'")
            source = os.path.normpath(source)
            if os.path.isdir(source):
                break
            print("❌ 源文件夹不存在，请重新输入！")

        while True:
            target_dir = input("请输入目标文件夹路径：").strip().strip('"').strip("'")
            target_dir = os.path.normpath(target_dir)
            if os.path.exists(target_dir):
                break
            print("❌ 目标文件夹不存在，请重新输入！")

        # 检查目标路径是否已存在同名文件夹
        target_path = os.path.join(target_dir, os.path.basename(source))

        if os.path.exists(target_path):
            print(f"⚠️ 目标位置已存在同名文件夹：{os.path.basename(source)}")
            #basename:从完整文件/文件夹路径中，提取最后一级名称（文件名或文件夹名）
            choice = input("请选择：1 → 覆盖并替换 / 2 → 合并文件夹 / 3 → 取消操作：").strip()

            if choice == '1':
                try:
                    shutil.rmtree(target_path)
                    shutil.move(source,target_dir)
                except Exception as e:
                    print(f"❌ 移动失败：{e}")
                    return
            elif choice == '2':
                #合并文件夹
                try:
                    merge_folders(source,target_path)
                    shutil.rmtree(source) #删除原文件夹
                    print(f"✅ 文件夹已合并移动成功！")
                except Exception as e:
                    print(f"❌ 合并失败：{e}")
                    return
            else:
                print("❌ 操作已取消")
                return
        else:
            try:
                shutil.move(source, target_dir)
                print(f"✅ 文件夹移动成功！")
                print(f"📂 从：{source}")
                print(f"📂 到：{target_path}")
            except Exception as e:
                print(f"❌ 移动失败：{e}")

    elif move_type == "3":
        # 批量移动文件（按后缀）
        print("\n批量移动文件（按后缀分类）")

        while True:
            source_dir = input("请输入源文件夹路径：").strip().strip('"').strip("'")
            source_dir = os.path.normpath(source_dir)
            if os.path.isdir(source_dir):
                break
            print("❌ 源文件夹不存在，请重新输入！")

        while True:
            target_base = input("请输入目标根目录：").strip().strip('"').strip("'")
            target_base = os.path.normpath(target_base)
            if os.path.exists(target_base):
                break
            print("❌ 目标根目录不存在，请重新输入！")

        # 输入要移动的后缀
        extensions = input("请输入要移动的文件后缀（多个用逗号分隔，如 .txt,.jpg，直接回车移动所有文件）：").strip()

        if extensions:
            ext_list = [ext.strip().lower() for ext in extensions.split(',')]
            # 原始输入：.TXT, jpg,.PNG
            # split(',') → [' .TXT ', ' .jpg', ' .PNG '] 这里是以英文逗号作为分隔符，把整串输入的extension切割为字符串列表
            # for ext in 切割后的列表,逐个取出分割后的每一段后缀字符串，命名为 ext, 以此遍历每个元素
            # strip() + lower() → ['.txt', '.jpg', '.png']
            # 最终得到列表：ext_list = ['.txt', '.jpg', '.png']
            ext_list = [ext if ext.startswith('.') else f'.{ext}' for ext in ext_list]
            #三元表达式：A if 条件 else B
            # 条件：ext.startswith('.')
            # 判断当前字符串是不是以英文点.开头(用户输入不规范：有人习惯写 txt，有人习惯写 .txt，这行代码统一补全后缀前面的点。)
            # 条件成立（已有点）：直接保留原字符串ext
            # 条件不成立（没有点）：用f - string在前面拼接一个点f'.{ext}'
        else:
            ext_list = None # 移动所有文件

        # 是否递归子文件夹
        recursive = input("是否递归搜索子文件夹？(y/n，默认y)：").strip().lower()
        recursive = recursive != 'n'

        # 是否保持目录结构
        keep_structure = input("是否保持目录结构？(y/n，默认y)：").strip().lower()
        keep_structure = keep_structure != 'n'

        print(f"\n🔄 正在扫描并移动文件...")

        moved_count = 0 #成功移动的文件总数，初始 0
        skipped_count = 0 #跳过不移动的文件总数（后缀不符合要求），初始 0
        error_count = 0 #移动失败的文件总数，初始 0

        def move_files_by_suffix(dir_path,relative_path=""):
            """
            relative_path="":带默认值的形参
            规则：调用函数时如果不传这个参数，它就自动使用 = 后面的默认值；如果调用时手动传了值，就用你传入的值，覆盖默认值
            我们用relative_path记录当前文件夹相对于原始根目录的层级路径。
            举例子：原始根目录：D:\素材（整个任务的起点）它本身没有上级目录，所以用空字符串表示「无层级」
            它下面的子文件夹子文件夹A：相对路径就是子文件夹A
            再下一级子文件夹B：相对路径就是子文件夹A\子文件夹B
            """


            nonlocal moved_count,skipped_count,error_count
            #nonlocal关键字:这个函数是嵌套函数，上面三个计数器定义在函数外面
            #修改外层函数的这三个变量，不是新建局部变量。没有这行，计数器数值永远不会变

            try:
                for name in os.listdir(dir_path):
                    full_path = os.path.join(dir_path,name) #拼接成完整绝对路径

                    if os.path.isfile(full_path):
                        should_move = False #should_move是标记位,默认先设为不移动
                        if ext_list is None:
                            should_move = True
                            #用户没输入后缀 → 移动所有文件
                        else:
                            suffix = os.path.splitext(name)[-1].lower()
                            if suffix in ext_list:
                                should_move = True
                                #判断当前文件后缀是否在用户指定列表里吗，在就标记为需要移动

                        if should_move: #看用户有没有保留目录结构的需求
                            if keep_structure and relative_path:
                                target_subdir = os.path.join(target_base,relative_path)
                            else:
                                target_subdir = target_base
                                """
                                场景 1：顶层文件夹（relative_path = ""）
                                keep_structure and "" → 结果为 False
                                执行 else，文件直接放到目标根目录，不新建子文件夹，符合预期。
                                场景 2：进入子文件夹（relative_path = "子文件夹 A"）
                                keep_structure and "子文件夹A" → 结果为 True
                                拼接路径、创建对应子目录，保留原结构。
                                """

                            os.makedirs(target_subdir,exist_ok=True)
                            target_path = os.path.join(target_subdir, name)
                            target_path = handle_duplicate_file(target_path)

                            try:
                                shutil.move(full_path, target_path)
                                moved_count += 1
                                print(f"  ✅ 已移动：{name} → {os.path.relpath(target_path, target_base)}")

                            except Exception as e:
                                error_count += 1
                                print(f"  ❌ 移动失败：{name} - {e}")
                        else:
                            skipped_count += 1

                    elif os.path.isdir(full_path) and recursive:
                        # 递归处理子文件夹
                        new_rel_path = os.path.join(relative_path, name) if keep_structure else ""
                        """
                        情况 1：keep_structure = True（用户选择「保留原有目录结构」）
                        把每一层文件夹名都拼接起来，完整记录原始层级，后续移动文件时，就会在目标目录复刻一模一样的文件夹结构
                        情况 2：keep_structure = False（用户选择「不保留目录结构」）
                        直接赋值：new_rel_path = ""
                        相对路径置为空，代表抛弃原有文件夹层级，后续所有文件都会直接平铺放到目标根目录，不会创建子文件夹
                        """
                        move_files_by_suffix(full_path, new_rel_path)

            except PermissionError:
                print(f"⚠️ 权限不足，无法访问：{dir_path}")
            except Exception as e:
                print(f"⚠️ 访问{dir_path}时出错：{e}")

        # 开始批量移动
        move_files_by_suffix(source_dir)#函数调用完成了，这里开始调用自身函数

        # 显示结果
        print(f"\n📊 批量移动完成！")
        print(f"  ✅ 成功移动：{moved_count} 个文件")
        if skipped_count > 0:
            print(f"  ⏭️ 已跳过：{skipped_count} 个文件（后缀不匹配）")
        if error_count > 0:
            print(f"  ❌ 移动失败：{error_count} 个文件")


#补充：什么时候用exists，什么时候用isfile和isdir
#exists 只能证明「路径有东西」，但分不清是文件还是文件夹
#而isfile和isdir要确保路径存在的同时并判断是否为文件或者文件夹

# 辅助函数：处理重名文件
def handle_duplicate_file(file_path):
    """处理重名文件，返回不冲突的文件路径"""

    # 1. 判断：目标文件不存在
    if not os.path.exists(file_path):
        return file_path # 路径可用，直接原路返回

    base, ext = os.path.splitext(file_path) #把完整路径拆分为 主文件名 + 后缀名；
    counter = 1 #用来给重复文件加序号

    while True:
        new_path = f"{base}_{counter}{ext}" # 拼接新路径：原名称_序号.后缀
        if not os.path.exists(new_path):
            print(f"⚠️ 文件已存在，自动重命名为：{os.path.basename(new_path)}")
            return new_path
        counter += 1
        """
        原路径：E:\目标\图片.jpg，该文件已存在
        第一次循环：new_path = E:\目标\图片_1.jpg,如果 图片_1.jpg 也存在 → counter 变成 2；
        循环生成 图片_2.jpg、图片_3.jpg…… 直到找到不存在的路径；
        """


#辅助函数：合并文件夹
def merge_folders(src_folder,dst_folder):
    """合并两个文件夹的内容"""
    os.makedirs(dst_folder, exist_ok=True)
    #exist_ok=True：如果目标文件夹已经存在，不报错、不重复创建，直接使用现有文件夹
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder,item)
        dst_path = os.path.join(dst_folder,item)

        if os.path.isdir(src_path):
            merge_folders(src_path,dst_path)
        else:
            #处理同名文件
            if os.path.exists(dst_path):
                dst_path = handle_duplicate_file(dst_path)
            shutil.move(src_path,dst_path)
    print(f"✅ 已合并文件夹：{src_folder} → {dst_folder}")





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
                                #这里不需要else的原因：这里在for循环里面，符合条件则收入列表，不符合则下一个
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
def func11_compress_file():
    print("\n===== 功能11：文件压缩 =====")

    #选择文件压缩类型
    print("压缩类型：")
    print("1 → 压缩单个文件")
    print("2 → 压缩整个文件夹")
    compress_type = input("请选择（1/2）：").strip()

    if compress_type not in['1','2']:
        print("❌ 输入无效")
        return

    source_path = ""
    #先定义变量，占个位置，保证后面一定能用，可以不写也没问题，可能会有黄色警告
    #因为后续要多次使用、在不同分支里赋值 → 必须提前初始化
    #只在一个地方用、用完就丢 → 可不用提前写

    if compress_type == "1":
        while True:
            source_path = input("请输入要压缩的文件的完整路径：").strip().strip('"').strip("'")
            source_path = os.path.normpath(source_path)
            if os.path.isfile(source_path):
                break
            print("❌ 文件不存在，请重新输入！")

        #自动生成压缩文件名
        default_zip_name = os.path.basename(source_path) + ".zip"
        #os.path.basename 获取文件 / 文件夹名字

    else:
        while True:
            source_path = input("请输入要压缩的文件夹路径：").strip().strip('"').strip("'")
            source_path = os.path.normpath(source_path)
            if os.path.isdir(source_path):
                break
            print("❌ 文件夹不存在，请重新输入！")

        default_zip_name = os.path.basename(source_path) + ".zip"
        #basename = 从完整路径里，只提取最后的文件名

    #获取文件保存路径
    target_dir = input(f"请输入压缩文件保存目录（直接回车保存到源文件所在目录）：").strip().strip('"').strip("'")
    #用户直接回车 → 保存到源文件同级目录
    if not target_dir:
        target_dir = os.path.dirname(source_path)

    target_dir = os.path.normpath(target_dir)
    if not os.path.exists(target_dir):
        print("❌ 目标目录不存在")
        return

    #获取压缩文件名
    zip_name = input(f"请输入压缩文件名（直接回车使用默认：{default_zip_name}）：").strip()
    if not zip_name:
        zip_name = default_zip_name
    if not zip_name.endswith('.zip'):
        zip_name += '.zip'
    #不输入 → 用默认名,忘记加 .zip → 自动补上
    zip_path = os.path.join(target_dir,zip_name)

    #判断是否已经存在
    if os.path.exists(zip_path):
        overwrite = input("⚠️ 文件已存在，是否覆盖？(y/n)：").strip().lower()
        if overwrite != 'y':
            print("❌ 压缩已取消")
            return

    #设置压缩等级
    compress_level = input("压缩等级（1-9，数值越大压缩率越高但速度越慢，默认6）：").strip()
    try: #对于可能出现错误的情况，使用try来尝试，如果出现异常报错，用except来抛出解决它
        compress_level = int(compress_level) if compress_level else 6
        #三元表达式：如果compress_level有效输入则转为整型int，否则则默认为6
        compress_level = max(1,min(9,compress_level)) #限制到1-9之间
    except ValueError:
        compress_level = 6
        #如果用户乱输入，int(compress_level)会出现ValueError
        #这个时候把compress_level默认变成6

    # 执行压缩
    print(f"🔄 正在压缩，请稍候...")
    try:
        with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zipf:
            # zipfile.ZipFile,创建 / 打开一个 zip 压缩包
            # 'w',write 写入模式,没有文件就创建,有文件就覆盖（前面已经确认过）
            # zipfile.ZIP_DEFLATED表示启用压缩,不写这个 → 只打包但不压缩,写了才能真正变小
            # as zipf,给压缩包起个小名 zipf,后面所有操作都用 zipf.xxx
            # with ... 的作用:自动打开、自动关闭文件,不用写 zipf.close()
            if compress_type == "1":
                #压缩单个文件
                zipf.write(source_path,arcname=os.path.basename(source_path),
                           compresslevel=compress_level)
                #压缩包（一个空箱子）,write() = 把东西放进箱子里
                #arcname = 压缩包里面显示的文件名,用basename()来缩短真实路径：例如：C:\folder\sub\a.txt变成简单的a.txt
            else:
                #压缩文件夹
                for root,dirs,files in os.walk(source_path):
                    # os.walk功能：自动遍历文件夹 + 所有子文件夹dirs + 所有文件files
                    # 返回3个东西：root(当前正在遍历的文件夹路径);dirs(当前文件夹里的子文件夹);files(当前文件夹里的所有文件)
                    for file in files:
                        file_path = os.path.join(root,file)
                        arcname = os.path.relpath(file_path,start=os.path.dirname(source_path))
                        '''
                        #os.path.relpath (文件，起点):计算从起点到文件的相对路径
                        让压缩包里的目录结构正确，不乱七八糟
                        例子：
                        源文件夹：C:/project/files
                        文件：C:/project/files/a/b/c.txt
                        相对路径变成：
                        files/a/b/c.txt
                        '''
                        zipf.write(file_path,arcname=arcname,compresslevel=compress_level)
        #显示压缩结果
        original_size = get_folder_size(source_path) if compress_type == "2" else os.path.getsize(source_path)
        compressed_size = os.path.getsize(zip_path)
        ratio = (1 - compressed_size / original_size)*100 if original_size > 0 else 0

        print(f"\n✅ 压缩成功！")
        print(f"📦 压缩文件：{zip_path}")
        print(f"📊 原始大小：{format_file_size(original_size)}")
        print(f"📊 压缩后：{format_file_size(compressed_size)}")
        print(f"📊 压缩率：{ratio:.1f}%")

        # 日志记录
        # log_operation("文件压缩", f"{source_path} → {zip_path}")

    except Exception as e:
        print(f"❌ 压缩失败：{e}")
        if os.path.exists(zip_path):
            os.remove(zip_path)

# 辅助函数：获取文件夹大小
def get_folder_size(folder_path):
    #递归计算文件夹总大小
    total_size = 0
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                    #获取这个文件的大小,total_size += = 加到总数里

                except (OSError,PermissionError):
                    pass #有些文件打不开、权限不够,跳过它，不算它，不报错
    except Exception:
        pass #整个文件夹遍历出错（比如文件夹不存在）,也直接跳过，不崩溃
    return total_size


#功能12：文件解压
def func12_extract_file():
    print("\n===== 功能12：文件解压 =====")

    #获取压缩文件路径
    while True:
        zip_path = input("请输入要解压的zip文件路径：").strip().strip("'").strip('"')
        zip_path = os.path.normpath(zip_path)
        if os.path.isfile(zip_path) and zip_path.lower().endswith('.zip'):
            break
        print("❌ 文件不存在或不是zip文件，请重新输入！")

    #验证zip文件是否有效
    try:
        with zipfile.ZipFile(zip_path,'r') as test_zip: #尝试打开这个压缩包
            pass #pass,什么都不做，只用来 “试打开”,只要能打开，就说明 ZIP 是好的
    except zipfile.BadZipFile:
        print("❌ 文件已损坏或不是有效的zip文件")
        return

    #获取解压目标路径
    default_extract_dir = os.path.splitext(zip_path)[0]
    #splitext的作用是分割这个路径和扩展名(后缀)，[0]的意思是取文件名主体，[1]是指取后缀
    #C:\project\archive.zip 被splitext之后，成为C:\project\archive（文件名主体） 和.zip（扩展名）
    extract_dir = input(f"请输入解压目标路径（直接回车使用：{default_extract_dir}）：").strip().strip('"').strip("'")

    if not extract_dir:
        extract_dir = default_extract_dir

    extract_dir = os.path.normpath(extract_dir)

    #检查是否已存在
    if os.path.exists(extract_dir):
        print("⚠️ 目标路径已存在")

        options = {
            "1": "overwrite",
            "2": "merge",
            "3": "cancel"
        }

        while True:
            choice = input("请选择：1 → 覆盖并清空 / 2 → 合并文件 / 3 → 取消操作：").strip()

            if choice in options:
                if choice == '1':
                    #删除现有文件夹
                    try:
                        shutil.rmtree(extract_dir)
                    except Exception as e:
                        print(f"❌ 删除失败：{e}")
                        return
                elif choice == '2':
                    print("📂 将合并到现有文件夹")
                elif choice == '3':
                    print("❌ 解压已取消")
                    return
                break #break 和所有 choice == 1/2/3 是同级的！只要 choice 是 1、2、3 其中一个，就会走到 break！

            else:
                print("❌ 输入无效，请重新选择（1/2/3）")

    #创建解压目录
    os.makedirs(extract_dir,exist_ok= True)

    #设置解压选项
    print("\n解压选项：")
    print("1 → 解压所有文件（默认）")
    print("2 → 仅解压特定类型文件（如 .txt, .jpg）")
    print("3 → 查看压缩包内容")

    sub_choice = input("请选择（直接回车使用选项1）：").strip()

    try:
        with zipfile.ZipFile(zip_path,'r') as zipf:
            if sub_choice == '3':
                print(f"\n📦 压缩包内容(共{len(zipf.namelist())}个文件:")
                print("=" * 60)
                for i,name in enumerate(zipf.namelist(),1):
                    info = zipf.getinfo(name) #拿到这个文件的大小、时间、是否为文件夹等信息
                    if not name.endswith('/'):
                        size_str = format_file_size(info.file_size)
                        print(f"{i:3d}. {name} ({size_str})")
                    else:
                        print(f"{i:3d}. {name} [文件夹]")

                confirm = input("\n是否解压？(y/n)：").strip().lower()
                if confirm != 'y':
                    print("❌ 解压已取消")
                    return

            elif sub_choice == '2':
                # 仅解压特定类型
                extensions = input("请输入要解压的文件扩展名（多个用逗号分隔，如 .txt,.jpg）：").strip()
                ext_list = [ext.strip().lower() for ext in extensions.split(',')]
                #split(',') → 按逗号切分,输入 .txt, .jpg→ 变成 ['.txt', '.jpg']
                files_to_extract = []
                for name in zipf.namelist():
                    if not name.endswith('/') and any(name.lower().endswith(ext) for ext in ext_list):
                        files_to_extract.append(name)

                if not files_to_extract:
                    print("❌ 压缩包中没有匹配的文件类型")
                    return

                print(f"找到 {len(files_to_extract)} 个匹配的文件")
                for name in files_to_extract:
                    zipf.extract(name,extract_dir)
                    #zipf.extract(文件名, 目标路径)：解压单个指定文件到对应目录
                    print(f"✅ 已解压：{name}")

            else:
                # 解压所有文件
                zipf.extractall(extract_dir)
                # extractall(目标路径)：一次性解压压缩包内全部文件与目录，自动还原原有文件夹结构
                print("✅ 所有文件解压完成")

    except Exception as e:
        print(f"❌ 解压失败：{e}")













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
        print("11 → 文件压缩")
        print("12 → 文件解压")
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
        elif choice == "11":
            func11_compress_file()
        elif choice == "12":
            func12_extract_file()

        elif choice == "0":
            print("程序退出，再见！")
            break
        else:
            print("输入错误，请重新选择！")

if __name__ == "__main__":
    main()
