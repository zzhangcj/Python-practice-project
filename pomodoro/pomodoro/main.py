"""番茄钟桌面应用入口。

用法：
    python -m pomodoro
    python pomodoro/main.py
"""

from pomodoro.app import PomodoroApp


def run():
    PomodoroApp().run()


if __name__ == '__main__':
    run()
