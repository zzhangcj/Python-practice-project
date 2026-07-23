import os
import shutil
import datetime

from config import LOG_FILE
from utils.path_utils import input_path, normalize_path
from utils.helpers import handle_duplicate_file, safe_input
from utils.logger import write_log


# ===== 功能1：查看文件夹内所有文件 =====
def func1_show_files():
    print("\n===== 功能1：查看文件夹内所有文件 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    while True:
        path = input_path("请输入你要查看的文件夹：")
        if os.path.isdir(path):
            break
        print("输入的路径错误，请重新输入！")

    file_list = []
    for name in os.listdir(path):
        full_name = os.path.join(path, name)
        if os.path.isfile(full_name):
            file_list.append(name)

    print("你要查看的文件夹内的文件如下：")
    for f in file_list:
        print(f)


# ===== 功能2：识别文件后缀 =====
def func2_get_suffix():
    print("\n===== 功能2：识别文件后缀 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    while True:
        path = input_path("请输入文件地址：")
        if os.path.exists(path):
            break
        print("路径输入错误！")

    suffix_dict = {}
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path):
            suffix = os.path.splitext(name)[-1].lower()
            if suffix not in suffix_dict:
                suffix_dict[suffix] = []
            suffix_dict[suffix].append(name)

    print("\n文件后缀分类结果：")
    for suf, files in suffix_dict.items():
        print(f"\n【{suf}】类型文件：")
        for f in files:
            print(f)


# ===== 功能3：自动创建文件夹 =====
def func3_make_folder():
    print("\n===== 功能3：自动创建文件夹 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    path = input_path("请输入你要在那里创建文件夹（路径）：")
    if not os.path.exists(path):
        print("路径不存在！")
        return

    folder_path = safe_input("请输入新的文件夹名称：").strip()
    new_folder = os.path.join(path, folder_path)

    if not os.path.exists(new_folder):
        try:
            os.mkdir(new_folder)
            print(f"✅ 文件夹创建成功：{new_folder}")
        except Exception as e:
            print(f"❌ 文件夹创建失败：{e}")
    else:
        print("⚠️ 文件夹已存在，无需创建")


# ===== 功能5：复制文件 =====
def func5_copy_file():
    print("\n===== 功能5：复制文件 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    while True:
        source = input_path("请输入要复制的文件完整路径：")
        if os.path.isfile(source):
            break
        print("❌ 源文件不存在，请重新输入！")

    while True:
        target_dir = input_path("请输入目标文件夹路径：")
        if os.path.exists(target_dir):
            break
        print("❌ 目标文件夹不存在，请重新输入！")

    try:
        # 处理目标路径中的同名文件
        target_path = os.path.join(target_dir, os.path.basename(source))
        target_path = handle_duplicate_file(target_path)
        shutil.copy2(source, target_path)
        print("✅ 文件复制成功！")
        print(f"📂 从：{source}")
        print(f"📂 到：{target_path}")
    except Exception as e:
        print(f"❌ 复制失败：{e}")


# ===== 功能6：删除文件 =====
def func6_delete_file():
    print("\n===== 功能6：删除文件 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    while True:
        file_path = input_path("请输入要删除的文件完整路径：")
        if os.path.isfile(file_path):
            break
        print("❌ 文件不存在，请重新输入！")

    confirm = safe_input("确定要删除吗？(y/n):")
    if confirm.lower() == "y":
        try:
            os.remove(file_path)
            print("✅ 文件删除成功！")
        except PermissionError:
            print("❌ 权限不足，无法删除文件！")
        except Exception as e:
            print(f"❌ 文件删除失败：{e}")
    else:
        print("❌ 文件删除取消！")


# ===== 功能7：删除文件夹 =====
def func7_delete_folder():
    print("\n===== 功能7：删除文件夹 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    while True:
        folder_path = input_path("请输入要删除的文件夹完整路径：")
        if os.path.isdir(folder_path):
            break
        print("❌ 文件夹不存在，请重新输入！")

    confirm = safe_input("确定要删除文件夹（包含里面所有文件）吗？(y/n):")
    if confirm.lower() == "y":
        try:
            shutil.rmtree(folder_path)
            print("✅ 文件夹删除成功！")
        except PermissionError:
            print("❌ 权限不足，无法删除文件夹！")
        except Exception as e:
            print(f"❌ 文件夹删除失败：{e}")
    else:
        print("❌ 文件夹删除取消！")


# ===== 功能8：文件重命名 =====
def func8_rename_file():
    print("\n===== 功能8：文件重命名 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    while True:
        file_path = input_path("请输入要重命名的文件完整路径：")
        if os.path.isfile(file_path):
            break
        print("❌ 文件不存在，请重新输入！")

    new_name = safe_input("请输入新的文件名（包含后缀）：").strip()
    if not new_name:
        print("❌ 文件名不能为空！")
        return

    new_path = os.path.join(os.path.dirname(file_path), new_name)

    # 检查目标文件是否已存在，防止覆盖
    if os.path.exists(new_path):
        print(f"⚠️ 目标文件名已存在：{new_name}")
        choice = safe_input("请选择：1 → 覆盖 / 2 → 取消：").strip()
        if choice != '1':
            print("❌ 重命名已取消")
            return

    try:
        os.rename(file_path, new_path)
        print("✅ 文件重命名成功！")
    except PermissionError:
        print("❌ 权限不足，无法重命名！")
    except Exception as e:
        print(f"❌ 重命名失败：{e}")


# ===== 功能9：日志输出 =====
def func9_log_output():
    print("\n===== 功能9：日志输出 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")
    log_content = safe_input("请输入要输出的日志内容：")
    if not log_content:
        print("❌ 日志内容不能为空")
        return

    log_line = write_log(log_content)
    print(f"✅ 日志已经保存！文件路径：{os.path.abspath(LOG_FILE)}")
    print("日志内容预览：", log_line.strip())
