"""纯逻辑定时器状态机。

不包含任何 UI 代码，仅通过回调与外部通信。
使用 tk.after() 实现 1 秒精度的倒计时。
"""

from pomodoro.constants import (
    DEFAULT_WORK_MIN, DEFAULT_SHORT_BREAK_MIN, DEFAULT_LONG_BREAK_MIN,
    LONG_BREAK_INTERVAL, MODE_CONFIG,
)


class PomodoroTimer:
    """番茄钟定时器状态机。

    状态: IDLE → RUNNING ⇄ PAUSED
    模式: WORK → SHORT_BREAK (或 LONG_BREAK) → WORK → ...
    """

    IDLE, RUNNING, PAUSED = 0, 1, 2
    WORK, SHORT_BREAK, LONG_BREAK = 0, 1, 2

    # 从 constants 提取的快捷查找表（供 UI 层使用）
    MODE_LABELS = {m: MODE_CONFIG[m]['label'] for m in MODE_CONFIG}
    MODE_COLORS = {m: MODE_CONFIG[m]['color'] for m in MODE_CONFIG}
    MODE_HOVER = {m: MODE_CONFIG[m]['hover'] for m in MODE_CONFIG}

    def __init__(self, root):
        self._root = root
        self.durations = {
            self.WORK: DEFAULT_WORK_MIN * 60,
            self.SHORT_BREAK: DEFAULT_SHORT_BREAK_MIN * 60,
            self.LONG_BREAK: DEFAULT_LONG_BREAK_MIN * 60,
        }
        self.state = self.IDLE
        self.mode = self.WORK
        self.remaining = self.durations[self.WORK]
        self.total = self.durations[self.WORK]
        self.session = 0
        self._job_id = None

        # 回调函数（由 UI 层绑定）
        self.on_tick = None       # (mins, secs, progress, mode)
        self.on_finish = None     # (next_mode)
        self.on_mode_change = None  # (new_mode)

    @property
    def progress(self):
        """当前进度 0.0 ~ 1.0"""
        if self.total <= 0:
            return 0
        return (self.total - self.remaining) / self.total

    @property
    def completed_sessions(self):
        """已完成的番茄钟数量"""
        return self.session

    def set_duration(self, mode, minutes):
        """设置指定模式的时长（分钟），自动转为秒"""
        self.durations[mode] = max(1, int(minutes)) * 60

    def switch_mode(self, mode):
        """手动切换到指定模式并重置为空闲状态"""
        self.pause()
        self.state = self.IDLE
        self.mode = mode
        self.remaining = self.durations[mode]
        self.total = self.durations[mode]
        self._notify_tick()
        if self.on_mode_change:
            self.on_mode_change(mode)

    def start(self):
        """开始或继续计时"""
        if self.state == self.IDLE:
            self.remaining = self.durations[self.mode]
            self.total = self.remaining
        self.state = self.RUNNING
        self._tick()

    def pause(self):
        """暂停计时"""
        if self.state != self.RUNNING:
            return
        self.state = self.PAUSED
        if self._job_id is not None:
            self._root.after_cancel(self._job_id)
            self._job_id = None

    def reset(self):
        """重置到初始状态（WORK 模式，空闲）"""
        self.pause()
        self.state = self.IDLE
        self.mode = self.WORK
        self.session = 0
        self.remaining = self.durations[self.WORK]
        self.total = self.durations[self.WORK]
        self._notify_tick()
        if self.on_mode_change:
            self.on_mode_change(self.mode)

    # ---- 内部 ----

    def _tick(self):
        if self.state != self.RUNNING:
            return
        if self.remaining <= 0:
            self._finish()
            return
        self._notify_tick()
        self.remaining -= 1
        self._job_id = self._root.after(1000, self._tick)

    def _notify_tick(self):
        if self.on_tick:
            m, s = divmod(self.remaining, 60)
            self.on_tick(m, s, self.progress, self.mode)

    def _finish(self):
        """当前阶段结束，自动推进到下一模式"""
        self.state = self.IDLE
        self._job_id = None
        if self.mode == self.WORK:
            self.session += 1
            nxt = (
                self.LONG_BREAK
                if self.session % LONG_BREAK_INTERVAL == 0
                else self.SHORT_BREAK
            )
        else:
            nxt = self.WORK
        if self.on_finish:
            self.on_finish(nxt)
        self.mode = nxt
        self.remaining = self.durations[nxt]
        self.total = self.durations[nxt]
        if self.on_mode_change:
            self.on_mode_change(nxt)
        self._notify_tick()
