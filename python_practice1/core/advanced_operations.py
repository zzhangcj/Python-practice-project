import os
import shutil

from utils.path_utils import input_path, normalize_path
from utils.helpers import handle_duplicate_file, merge_folders, safe_input


# ===== 功能4：移动文件/文件夹 =====
def func4_move_file():
    print("\n===== 功能4：移动文件/文件夹 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")

    # 选择移动类型
    print("移动类型：")
    print("1 → 移动单个文件")
    print("2 → 移动文件夹")
    print("3 → 批量移动文件（按后缀）")
    move_type = safe_input("请选择（1/2/3）：").strip()

    if move_type == "1":
        # 移动单个文件
        while True:
            source = input_path("请输入要移动的文件完整路径：")
            if os.path.isfile(source):
                break
            print("❌ 源文件不存在，请重新输入！")

        while True:
            target_dir = input_path("请输入目标文件夹路径：")
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
            source = input_path("请输入要移动的文件夹完整路径：")
            if os.path.isdir(source):
                break
            print("❌ 源文件夹不存在，请重新输入！")

        while True:
            target_dir = input_path("请输入目标文件夹路径：")
            if os.path.exists(target_dir):
                break
            print("❌ 目标文件夹不存在，请重新输入！")

        # 检查目标路径是否已存在同名文件夹
        target_path = os.path.join(target_dir, os.path.basename(source))

        if os.path.exists(target_path):
            print(f"⚠️ 目标位置已存在同名文件夹：{os.path.basename(source)}")
            choice = safe_input("请选择：1 → 覆盖并替换 / 2 → 合并文件夹 / 3 → 取消操作：").strip()

            if choice == '1':
                try:
                    shutil.rmtree(target_path)
                    shutil.move(source, target_dir)
                except Exception as e:
                    print(f"❌ 移动失败：{e}")
                    return
            elif choice == '2':
                try:
                    merge_folders(source, target_path)
                    shutil.rmtree(source)
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
            source_dir = input_path("请输入源文件夹路径：")
            if os.path.isdir(source_dir):
                break
            print("❌ 源文件夹不存在，请重新输入！")

        while True:
            target_base = input_path("请输入目标根目录：")
            if os.path.exists(target_base):
                break
            print("❌ 目标根目录不存在，请重新输入！")

        # 输入要移动的后缀
        extensions = safe_input("请输入要移动的文件后缀（多个用逗号分隔，如 .txt,.jpg，直接回车移动所有文件）：").strip()

        if extensions:
            ext_list = [ext.strip().lower() for ext in extensions.split(',')]
            ext_list = [ext if ext.startswith('.') else f'.{ext}' for ext in ext_list]
        else:
            ext_list = None  # 移动所有文件

        # 是否递归子文件夹
        recursive = safe_input("是否递归搜索子文件夹？(y/n，默认y)：").strip().lower()
        recursive = recursive != 'n'

        # 是否保持目录结构
        keep_structure = safe_input("是否保持目录结构？(y/n，默认y)：").strip().lower()
        keep_structure = keep_structure != 'n'

        print(f"\n🔄 正在扫描并移动文件...")

        moved_count = 0
        skipped_count = 0
        error_count = 0

        def move_files_by_suffix(dir_path, relative_path=""):
            """
            递归扫描并移动文件的内部函数
            relative_path 记录当前文件夹相对于原始根目录的层级路径
            """
            nonlocal moved_count, skipped_count, error_count

            try:
                for name in os.listdir(dir_path):
                    full_path = os.path.join(dir_path, name)

                    if os.path.isfile(full_path):
                        should_move = False
                        if ext_list is None:
                            should_move = True
                        else:
                            suffix = os.path.splitext(name)[-1].lower()
                            if suffix in ext_list:
                                should_move = True

                        if should_move:
                            if keep_structure and relative_path:
                                target_subdir = os.path.join(target_base, relative_path)
                            else:
                                target_subdir = target_base

                            os.makedirs(target_subdir, exist_ok=True)
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
                        new_rel_path = os.path.join(relative_path, name) if keep_structure else ""
                        move_files_by_suffix(full_path, new_rel_path)

            except PermissionError:
                print(f"⚠️ 权限不足，无法访问：{dir_path}")
            except Exception as e:
                print(f"⚠️ 访问{dir_path}时出错：{e}")

        # 开始批量移动
        move_files_by_suffix(source_dir)

        # 显示结果
        print(f"\n📊 批量移动完成！")
        print(f"  ✅ 成功移动：{moved_count} 个文件")
        if skipped_count > 0:
            print(f"  ⏭️ 已跳过：{skipped_count} 个文件（后缀不匹配）")
        if error_count > 0:
            print(f"  ❌ 移动失败：{error_count} 个文件")
