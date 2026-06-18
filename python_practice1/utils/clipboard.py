import subprocess


# ===== 复制到剪贴板（跨平台，当前支持Windows） =====
def copy_to_clipboard(text):
    """
    复制文本到系统剪贴板
    Windows 使用 clip 命令；Linux/macOS 可扩展
    """
    try:
        subprocess.run(['clip'], input=text.strip().encode('gbk'), check=True)
    except Exception as e:
        print(f"⚠️ 复制失败：{e}")
