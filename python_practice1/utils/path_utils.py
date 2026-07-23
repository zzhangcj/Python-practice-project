import os

from utils.helpers import safe_input


def normalize_path(path):
    """标准化路径：去除引号、空白，规范化路径格式"""
    if not isinstance(path, str):
        return path
    return os.path.normpath(path.strip().strip('"').strip("'"))


def input_path(prompt):
    """带提示的路径输入并自动标准化，支持 q/0 退出"""
    return normalize_path(safe_input(prompt))
