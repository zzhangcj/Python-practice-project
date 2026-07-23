import os
import datetime

from utils.path_utils import input_path, normalize_path
from utils.helpers import format_file_size, export_search_result_to_log, safe_input
from utils.clipboard import copy_to_clipboard


# ===== 功能10：文件搜索 =====
def func10_file_search():
    print("\n===== 功能10：文件搜索 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")

    while True:
        search_path = input_path("请输入要搜索的文件夹路径：")
        if os.path.isdir(search_path):
            break
        print("输入的路径错误，请重新输入！")

    keyword = safe_input("请输入要搜索的文件名关键字：").strip()

    # 是否递归子文件夹
    recursive = safe_input("是否递归子文件夹？(y/n):").lower()
    recursive = recursive != 'n'

    # 是否区分大小写
    case_sensitive = safe_input("是否区分大小写？(y/n):").lower()
    case_sensitive = (case_sensitive == "y")

    print(f"正在搜索：{search_path} 关键字：{keyword}，递归：{recursive}，区分大小写：{case_sensitive}.....")
    result_files = []

    def search_in_dir(dir_path):
        try:
            for name in os.listdir(dir_path):
                full_path = os.path.join(dir_path, name)

                if os.path.isfile(full_path):
                    if keyword:
                        if case_sensitive:
                            if keyword in name:
                                result_files.append(full_path)
                        else:
                            if keyword.lower() in name.lower():
                                result_files.append(full_path)
                    else:
                        result_files.append(full_path)

                elif os.path.isdir(full_path) and recursive:
                    search_in_dir(full_path)
        except PermissionError:
            pass
        except Exception as e:
            print(f'访问{dir_path}时出错：{e}')

    # 开始搜索
    search_in_dir(search_path)

    # 显示结果
    if result_files:
        print(f"\n✅ 找到{len(result_files)}个文件：")
        print("=" * 60)
        for i, file_path in enumerate(result_files, 1):
            file_size = os.path.getsize(file_path)
            size_str = format_file_size(file_size)
            print(f"{i:3d}. {file_path}({size_str})")

        # 提供额外选项
        print("\n" + "=" * 60)
        print("额外选项：")
        print("1 → 导出搜索结果到日志")
        print("2 → 复制某个文件路径到剪贴板")
        print("0 → 返回主菜单")
        sub_choice = safe_input("请选择（直接回车返回主菜单）：").strip()

        if sub_choice == "1":
            export_search_result_to_log(result_files, search_path, keyword)
        elif sub_choice == "2":
            try:
                idx = int(safe_input(f"请输入要复制的文件编号（1-{len(result_files)}）："))
                if 1 <= idx <= len(result_files):
                    copy_to_clipboard(result_files[idx - 1])
                    print("✅ 路径已复制到剪贴板")
                else:
                    print("❌ 编号无效")
            except ValueError:
                print("❌ 输入无效")
    else:
        print(f"\n❌ 未找到匹配的文件（关键词：{keyword if keyword else '无'}）")
