import os
import shutil
import datetime

from config import SEARCH_RESULT_LOG


# ===== 辅助函数：处理重名文件 =====
def handle_duplicate_file(file_path):
    """处理重名文件，返回不冲突的文件路径"""
    if not os.path.exists(file_path):
        return file_path

    base, ext = os.path.splitext(file_path)
    counter = 1

    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            print(f"⚠️ 文件已存在，自动重命名为：{os.path.basename(new_path)}")
            return new_path
        counter += 1


# ===== 辅助函数：格式化文件大小 =====
def format_file_size(size_bytes):
    """将字节转换为可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"


# ===== 辅助函数：获取文件夹总大小 =====
def get_folder_size(folder_path):
    """递归计算文件夹总大小"""
    total_size = 0
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                except (OSError, PermissionError):
                    pass
    except Exception:
        pass
    return total_size


# ===== 辅助函数：合并文件夹 =====
def merge_folders(src_folder, dst_folder):
    """合并两个文件夹的内容"""
    os.makedirs(dst_folder, exist_ok=True)
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)

        if os.path.isdir(src_path):
            merge_folders(src_path, dst_path)
        else:
            # 处理同名文件
            if os.path.exists(dst_path):
                dst_path = handle_duplicate_file(dst_path)
            shutil.move(src_path, dst_path)
    print(f"✅ 已合并文件夹：{src_folder} → {dst_folder}")


# ===== 辅助函数：导出搜索结果到日志 =====
def export_search_result_to_log(result_files, search_path, keyword):
    """将搜索结果导出到日志文件"""
    log_path = SEARCH_RESULT_LOG
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
