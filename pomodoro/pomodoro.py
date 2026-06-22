"""番茄钟桌面应用（向后兼容入口）。

推荐用法：
    python pomodoro/main.py
    python -m pomodoro

此文件保留用于向后兼容：
    python pomodoro.py
"""

from pomodoro.main import run

if __name__ == '__main__':
    run()
