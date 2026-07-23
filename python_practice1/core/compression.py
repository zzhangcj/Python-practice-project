import os
import shutil
import zipfile

from config import DEFAULT_COMPRESS_LEVEL
from utils.path_utils import input_path, normalize_path
from utils.helpers import format_file_size, get_folder_size, safe_input


# ===== 功能11：文件压缩 =====
def func11_compress_file():
    print("\n===== 功能11：文件压缩 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")

    # 选择压缩类型
    print("压缩类型：")
    print("1 → 压缩单个文件")
    print("2 → 压缩整个文件夹")
    compress_type = safe_input("请选择（1/2）：").strip()

    if compress_type not in ['1', '2']:
        print("❌ 输入无效")
        return

    source_path = ""

    if compress_type == "1":
        while True:
            source_path = input_path("请输入要压缩的文件的完整路径：")
            if os.path.isfile(source_path):
                break
            print("❌ 文件不存在，请重新输入！")
        default_zip_name = os.path.basename(source_path) + ".zip"
    else:
        while True:
            source_path = input_path("请输入要压缩的文件夹路径：")
            if os.path.isdir(source_path):
                break
            print("❌ 文件夹不存在，请重新输入！")
        default_zip_name = os.path.basename(source_path) + ".zip"

    # 获取文件保存路径
    target_dir = safe_input("请输入压缩文件保存目录（直接回车保存到源文件所在目录）：").strip().strip('"').strip("'")
    if not target_dir:
        target_dir = os.path.dirname(source_path)
    else:
        target_dir = normalize_path(target_dir)

    if not os.path.exists(target_dir):
        print("❌ 目标目录不存在")
        return

    # 获取压缩文件名
    zip_name = safe_input(f"请输入压缩文件名（直接回车使用默认：{default_zip_name}）：").strip()
    if not zip_name:
        zip_name = default_zip_name
    if not zip_name.endswith('.zip'):
        zip_name += '.zip'
    zip_path = os.path.join(target_dir, zip_name)

    # 判断是否已存在
    if os.path.exists(zip_path):
        overwrite = safe_input("⚠️ 文件已存在，是否覆盖？(y/n)：").strip().lower()
        if overwrite != 'y':
            print("❌ 压缩已取消")
            return

    # 设置压缩等级
    compress_level = safe_input("压缩等级（1-9，数值越大压缩率越高但速度越慢，默认6）：").strip()
    try:
        compress_level = int(compress_level) if compress_level else DEFAULT_COMPRESS_LEVEL
        compress_level = max(1, min(9, compress_level))
    except ValueError:
        compress_level = DEFAULT_COMPRESS_LEVEL

    # 执行压缩
    print(f"🔄 正在压缩，请稍候...")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if compress_type == "1":
                # 压缩单个文件
                zipf.write(source_path, arcname=os.path.basename(source_path),
                           compresslevel=compress_level)
            else:
                # 压缩文件夹
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=os.path.dirname(source_path))
                        zipf.write(file_path, arcname=arcname, compresslevel=compress_level)

        # 显示压缩结果
        original_size = get_folder_size(source_path) if compress_type == "2" else os.path.getsize(source_path)
        compressed_size = os.path.getsize(zip_path)
        ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0

        print(f"\n✅ 压缩成功！")
        print(f"📦 压缩文件：{zip_path}")
        print(f"📊 原始大小：{format_file_size(original_size)}")
        print(f"📊 压缩后：{format_file_size(compressed_size)}")
        print(f"📊 压缩率：{ratio:.1f}%")

    except Exception as e:
        print(f"❌ 压缩失败：{e}")
        if os.path.exists(zip_path):
            os.remove(zip_path)


# ===== 功能12：文件解压 =====
def func12_extract_file():
    print("\n===== 功能12：文件解压 =====")
    print("提示：输入 q 或 0 可随时退出当前功能")

    # 获取压缩文件路径
    while True:
        zip_path = safe_input("请输入要解压的zip文件路径：").strip().strip("'").strip('"')
        zip_path = os.path.normpath(zip_path)
        if os.path.isfile(zip_path) and zip_path.lower().endswith('.zip'):
            break
        print("❌ 文件不存在或不是zip文件，请重新输入！")

    # 验证zip文件是否有效
    try:
        with zipfile.ZipFile(zip_path, 'r') as test_zip:
            pass
    except zipfile.BadZipFile:
        print("❌ 文件已损坏或不是有效的zip文件")
        return

    # 获取解压目标路径
    default_extract_dir = os.path.splitext(zip_path)[0]
    extract_dir = safe_input(f"请输入解压目标路径（直接回车使用：{default_extract_dir}）：").strip().strip('"').strip("'")

    if not extract_dir:
        extract_dir = default_extract_dir

    extract_dir = os.path.normpath(extract_dir)

    # 检查是否已存在
    if os.path.exists(extract_dir):
        print("⚠️ 目标路径已存在")

        while True:
            choice = safe_input("请选择：1 → 覆盖并清空 / 2 → 合并文件 / 3 → 取消操作：").strip()

            if choice == '1':
                try:
                    shutil.rmtree(extract_dir)
                except Exception as e:
                    print(f"❌ 删除失败：{e}")
                    return
                break
            elif choice == '2':
                print("📂 将合并到现有文件夹")
                break
            elif choice == '3':
                print("❌ 解压已取消")
                return
            else:
                print("❌ 输入无效，请重新选择（1/2/3）")

    # 创建解压目录
    try:
        os.makedirs(extract_dir, exist_ok=True)
    except Exception as e:
        print(f"❌ 创建目录失败：{e}")
        return

    # 设置解压选项
    print("\n解压选项：")
    print("1 → 解压所有文件（默认）")
    print("2 → 仅解压特定类型文件（如 .txt, .jpg）")
    print("3 → 查看压缩包内容")

    sub_choice = safe_input("请选择（直接回车使用选项1）：").strip()

    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            if sub_choice == '3':
                print(f"\n📦 压缩包内容（共{len(zipf.namelist())}个文件）：")
                print("=" * 60)
                for i, name in enumerate(zipf.namelist(), 1):
                    info = zipf.getinfo(name)
                    if not name.endswith('/'):
                        size_str = format_file_size(info.file_size)
                        print(f"{i:3d}. {name} ({size_str})")
                    else:
                        print(f"{i:3d}. {name} [文件夹]")

                confirm = safe_input("\n是否解压？(y/n)：").strip().lower()
                if confirm != 'y':
                    print("❌ 解压已取消")
                    return

            elif sub_choice == '2':
                extensions = safe_input("请输入要解压的文件扩展名（多个用逗号分隔，如 .txt,.jpg）：").strip()
                ext_list = [ext.strip().lower() for ext in extensions.split(',')]
                files_to_extract = []
                for name in zipf.namelist():
                    if not name.endswith('/') and any(name.lower().endswith(ext) for ext in ext_list):
                        files_to_extract.append(name)

                if not files_to_extract:
                    print("❌ 压缩包中没有匹配的文件类型")
                    return

                print(f"找到 {len(files_to_extract)} 个匹配的文件")
                for name in files_to_extract:
                    zipf.extract(name, extract_dir)
                    print(f"✅ 已解压：{name}")

            else:
                zipf.extractall(extract_dir)
                print("✅ 所有文件解压完成")

    except Exception as e:
        print(f"❌ 解压失败：{e}")
