import os
import shutil
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
        elif choice == "0":
            print("程序退出，再见！")
            break
        else:
            print("输入错误，请重新选择！")

if __name__ == "__main__":
    main()
