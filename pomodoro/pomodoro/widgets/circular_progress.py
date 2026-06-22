"""环形进度条（Canvas 绘制）。

特性：
- 暗色轨道弧线 + 彩色进度弧线
- 进度值平滑过渡（指数衰减动画）
- 轨道阴影 + 进度发光效果
- 模式切换时环宽脉冲动画
"""

import tkinter as tk
from pomodoro.constants import (
    BG_DEEP, RING_TRACK, SHADOW, TEXT_PRIMARY, TEXT_SECONDARY,
    FONT_TIME, FONT_MODE_LABEL, ANIM_FRAME_MS, PROGRESS_DECAY,
    PULSE_DURATION_MS, PULSE_WIDTH_DELTA, MODE_CONFIG,
)


class CircularProgressBar(tk.Canvas):
    """环形进度条，显示倒计时圆环。

    使用两层弧线：底层暗色轨道 + 顶层彩色进度。
    值变化时以指数衰减方式平滑过渡，避免跳变。
    """

    def __init__(self, parent, size=280, ring_width=18, **kw):
        super().__init__(parent, width=size, height=size,
                         bg=BG_DEEP, highlightthickness=0, **kw)
        self._size = size
        self._cx = size // 2
        self._cy = size // 2
        self._mid_r = (size // 2) - 10          # 弧线中线半径
        self._width = ring_width
        self._base_width = ring_width           # 保存基础环宽（脉冲后恢复）

        # 当前正在显示的值（会被动画平滑推进）
        self._display_val = 0.0
        self._target_val = 0.0
        self._color = MODE_CONFIG[0]['color']
        self._time_str = '00:00'
        self._mode_str = ''

        # 动画控制
        self._anim_job = None

    def set_value(self, percent, color=None, time_str=None, mode_str=None):
        """设定目标进度值，动画平滑过渡到此值。

        Args:
            percent: 0-100 的进度百分比
            color: 进度弧线颜色（不传则保持当前）
            time_str: 中央时间文字
            mode_str: 模式标签
        """
        self._target_val = max(0, min(100, percent))
        if color is not None:
            self._color = color
        if time_str is not None:
            self._time_str = time_str
        if mode_str is not None:
            self._mode_str = mode_str
        self._start_animation()

    def pulse(self):
        """模式切换脉冲：短暂加粗环宽后恢复。

        在模式切换或重置时调用，给用户视觉反馈。
        """

        def _shrink(step=0):
            delta = int(PULSE_WIDTH_DELTA * (1 - step / 6))
            self._width = self._base_width + delta
            self._redraw()
            if step < 6:
                self.after(PULSE_DURATION_MS // 6, lambda: _shrink(step + 1))

        _shrink()

    def _start_animation(self):
        """启动指数衰减动画（如已在运行则不重复创建）"""
        if self._anim_job:
            return
        self._tween_step()

    def _tween_step(self):
        diff = self._target_val - self._display_val
        if abs(diff) < 0.3:
            self._display_val = self._target_val
            self._redraw()
            self._anim_job = None
            return
        self._display_val += diff * PROGRESS_DECAY
        self._redraw()
        self._anim_job = self.after(ANIM_FRAME_MS, self._tween_step)

    def _redraw(self):
        """完整重绘环形进度条"""
        self.delete('all')

        # 坐标计算
        d = 2 * self._mid_r
        x1 = self._cx - self._mid_r
        y1 = self._cy - self._mid_r
        x2 = self._cx + self._mid_r
        y2 = self._cy + self._mid_r

        # ---- 阴影弧线（偏移 2px） ----
        self.create_arc(x1 + 2, y1 + 2, x2 + 2, y2 + 2,
                        start=90, extent=-360,
                        style='arc', width=self._width,
                        outline=SHADOW)

        # ---- 暗色轨道 ----
        self.create_arc(x1, y1, x2, y2,
                        start=90, extent=-360,
                        style='arc', width=self._width,
                        outline=RING_TRACK)

        # ---- 进度发光（宽半透明弧线） ----
        extent = -self._display_val * 360 / 100
        if abs(extent) > 0.5:
            fallback = {'glow': self._color}  # 无匹配时用原色
            glow_color = MODE_CONFIG.get(
                self._get_mode_by_color(self._color),
                fallback,
            )['glow']
            self.create_arc(x1, y1, x2, y2,
                            start=90, extent=extent,
                            style='arc', width=self._width + 8,
                            outline=glow_color)

        # ---- 进度弧线 ----
        if abs(extent) > 0.5:
            self.create_arc(x1, y1, x2, y2,
                            start=90, extent=extent,
                            style='arc', width=self._width,
                            outline=self._color)

        # ---- 中央时间文字 ----
        self.create_text(self._cx, self._cy - 6, text=self._time_str,
                         fill=TEXT_PRIMARY, font=FONT_TIME)

        # ---- 模式标签 ----
        self.create_text(self._cx, self._cy + 30, text=self._mode_str,
                         fill=TEXT_SECONDARY, font=FONT_MODE_LABEL)

    @staticmethod
    def _get_mode_by_color(color):
        """根据颜色反查模式 ID（用于发光颜色查找）"""
        for mode, cfg in MODE_CONFIG.items():
            if cfg['color'] == color:
                return mode
        return 0
