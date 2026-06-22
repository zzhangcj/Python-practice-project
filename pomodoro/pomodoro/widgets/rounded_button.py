"""圆角按钮（Canvas 绘制）。

特性：
- 自定义圆角矩形，圆角半径可配置
- hover 时颜色平滑过渡（RGB 指数衰减动画）
- 点击时短暂缩放反馈
- 按钮上半部轻微提亮，模拟顶光源渐变
"""

import tkinter as tk
from pomodoro.constants import (
    BG_BUTTON, TEXT_PRIMARY, BG_BUTTON_HOVER,
    TEXT_ON_ACCENT, ANIM_FRAME_MS, HOVER_ANIM_DECAY,
    PRESS_SCALE_MS, FONT_BUTTON_MAIN, BG_DEEP,
)


class RoundedButton(tk.Canvas):
    """Canvas 绘制的圆角矩形按钮。

    与 tk.Button 不同，此类完全控制绘制，
    因此可以自由设置圆角、渐变色和动画过渡。
    """

    def __init__(self, parent, text, width=100, height=36, radius=18,
                 bg=BG_BUTTON, fg=TEXT_PRIMARY, hover_bg=None,
                 command=None, font_spec=None, **kw):
        bg_color = BG_DEEP if 'highlightthickness' not in kw else kw.pop('bg')
        super().__init__(parent, width=width, height=height,
                         bg=bg_color, highlightthickness=0, **kw)
        self._btn_w = width
        self._btn_h = height
        self._btn_r = min(radius, height // 2)
        self._text = text
        self._bg_hex = bg
        self._fg = fg
        self._hover_bg_hex = hover_bg or bg
        self._command = command
        self._font_spec = font_spec or FONT_BUTTON_MAIN
        self._hovered = False
        self._pressed = False

        # 动画状态
        self._current_rgb = self._parse_hex(bg)
        self._target_rgb = self._current_rgb
        self._anim_job = None

        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        self._draw()

    # ---- 公开方法 ----

    def set_colors(self, bg_hex, fg, hover_bg_hex=None):
        """更换配色并立即重绘（不带动画）"""
        self._bg_hex = bg_hex
        self._fg = fg
        if hover_bg_hex is not None:
            self._hover_bg_hex = hover_bg_hex
        # 取消动画，直接跳到目标色
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        target = self._hover_bg_hex if self._hovered else bg_hex
        self._current_rgb = self._parse_hex(target)
        self._target_rgb = self._current_rgb
        self._draw()

    def set_text(self, text):
        """更换按钮文字"""
        self._text = text
        self._draw()

    # ---- 内部绘制 ----

    def _draw(self):
        """完整重绘按钮"""
        self.delete('all')
        # 按下时缩小 2px
        offset = 2 if self._pressed else 0
        w, h = self._btn_w - offset * 2, self._btn_h - offset * 2
        ox, oy = offset, offset

        fill = self._rgb_to_hex(self._current_rgb)
        # 渐变：上半部浅色→下半部深色
        lighter = self._lighten_rgb(self._current_rgb, 0.08)

        # 下半部（深色）
        self._round_rect(ox, oy + h // 2, ox + w, oy + h,
                         self._btn_r, fill=fill, outline='')
        # 上半部（浅色）
        self._round_rect(ox, oy, ox + w, oy + h // 2,
                         self._btn_r, fill=self._rgb_to_hex(lighter), outline='')
        # 覆盖一层完整形状以消除中间接缝（只画轮廓再填充会导致接缝可见）
        # 重新画完整形状但使用透明叠加 —— 这里直接用原色画完整按钮然后上半部浅色叠在上面
        # 简化：画完整按钮 + 上半部浅色矩形覆盖
        self._round_rect(ox, oy, ox + w, oy + h, self._btn_r,
                         fill=fill, outline='')
        self.create_rectangle(
            ox, oy, ox + w, oy + h // 2,
            fill=self._rgb_to_hex(lighter), outline='',
        )
        # 用弧形修复上部矩形在圆角处的溢出
        d = 2 * self._btn_r
        if d > 0:
            self.create_arc(ox, oy, ox + d, oy + d, start=90, extent=90,
                            style='pieslice', fill=self._rgb_to_hex(lighter), outline='')
            self.create_arc(ox + w - d, oy, ox + w, oy + d, start=0, extent=90,
                            style='pieslice', fill=self._rgb_to_hex(lighter), outline='')

        # 文字
        cx, cy = ox + w // 2, oy + h // 2
        # 根据背景亮度选择文字色（亮底用深字，暗底用浅字）
        text_color = self._fg
        self.create_text(cx, cy, text=self._text, fill=text_color,
                         font=self._font_spec)

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        """画圆角矩形"""
        d = 2 * r
        self.create_arc(x1, y1, x1 + d, y1 + d, start=90, extent=90,
                        style='pieslice', **kw)
        self.create_arc(x2 - d, y1, x2, y1 + d, start=0, extent=90,
                        style='pieslice', **kw)
        self.create_arc(x1, y2 - d, x1 + d, y2, start=180, extent=90,
                        style='pieslice', **kw)
        self.create_arc(x2 - d, y2 - d, x2, y2, start=270, extent=90,
                        style='pieslice', **kw)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, **kw)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, **kw)

    # ---- 动画 ----

    def _animate_to(self, target_hex):
        """平滑过渡到目标颜色（指数衰减）"""
        self._target_rgb = self._parse_hex(target_hex)
        if not self._anim_job:
            self._tween_color_step()

    def _tween_color_step(self):
        r, g, b = self._current_rgb
        tr, tg, tb = self._target_rgb
        dr, dg, db = tr - r, tg - g, tb - b
        if abs(dr) < 2 and abs(dg) < 2 and abs(db) < 2:
            self._current_rgb = self._target_rgb
            self._draw()
            self._anim_job = None
            return
        decay = HOVER_ANIM_DECAY
        self._current_rgb = (
            r + dr * decay,
            g + dg * decay,
            b + db * decay,
        )
        self._draw()
        self._anim_job = self.after(ANIM_FRAME_MS, self._tween_color_step)

    # ---- 事件 ----

    def _on_enter(self, e):
        self._hovered = True
        self._animate_to(self._hover_bg_hex)

    def _on_leave(self, e):
        self._hovered = False
        self._animate_to(self._bg_hex)

    def _on_click(self, e):
        # 按下动画
        self._pressed = True
        self._draw()
        self.after(PRESS_SCALE_MS, self._release_press)
        if self._command:
            self._command()

    def _release_press(self):
        self._pressed = False
        self._draw()

    # ---- 颜色工具 ----

    @staticmethod
    def _parse_hex(hex_color):
        """#rrggbb → (r, g, b) 0-255"""
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(rgb):
        """(r, g, b) → '#rrggbb'"""
        return '#{:02x}{:02x}{:02x}'.format(
            int(max(0, min(255, rgb[0]))),
            int(max(0, min(255, rgb[1]))),
            int(max(0, min(255, rgb[2]))),
        )

    @staticmethod
    def _lighten_rgb(rgb, amount):
        """将 RGB 各通道提亮指定比例（0~1）"""

        def _f(c):
            return min(255, int(c + (255 - c) * amount))

        return (_f(rgb[0]), _f(rgb[1]), _f(rgb[2]))
