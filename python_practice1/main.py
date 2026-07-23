#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件小工具 - 程序入口
仅存放主菜单循环和功能路由调度
"""

from core.file_operations import (
    func1_show_files, func2_get_suffix, func3_make_folder,
    func5_copy_file, func6_delete_file, func7_delete_folder,
    func8_rename_file, func9_log_output
)
from core.advanced_operations import func4_move_file
from core.search import func10_file_search
from core.compression import func11_compress_file, func12_extract_file
from utils.helpers import ReturnToMenu


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

        try:
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
        except ReturnToMenu:
            pass  # 已在 safe_input 中打印退出提示，直接回到主菜单循环


if __name__ == "__main__":
    main()
