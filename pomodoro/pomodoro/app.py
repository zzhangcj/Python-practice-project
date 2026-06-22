"""番茄钟主窗口。

负责组装所有 UI 组件、连线计时器回调、管理系统托盘。
布局采用三层卡片结构：模式切换栏 → 进度环 → 操作按钮。
"""

import tkinter as tk
import threading
import winsound
from PIL import Image, ImageDraw
import pystray

from pomodoro.constants import (
    BG_DEEP, BG_CARD, BG_BUTTON, BG_BUTTON_HOVER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, TEXT_ON_ACCENT,
    SHADOW, TRAY_ICON_COLOR,
    FONT_SESSION, FONT_BUTTON_MAIN, FONT_BUTTON_MODE,
    WIN_W, WIN_H, PADDING,
    RING_SIZE, RING_WIDTH,
    MODE_BTN_W, MODE_BTN_H, MODE_BTN_RADIUS, MODE_BTN_GAP,
    GEAR_BTN_SIZE,
    ACTION_BTN_W, ACTION_BTN_H, ACTION_BTN_RADIUS,
    RESET_BTN_W, RESET_BTN_H, RESET_BTN_RADIUS,
    SESSION_PILL_W, SESSION_PILL_H,
    MODE_CONFIG,
)
from pomodoro.timer import PomodoroTimer
from pomodoro.widgets.rounded_button import RoundedButton
from pomodoro.widgets.circular_progress import CircularProgressBar
from pomodoro.settings import SettingsWindow


class PomodoroApp:
    """番茄钟应用主窗口。

    拥有计时器实例并绑定其回调，管理所有 UI 组件和系统托盘。
    """

    MINI_TITLE = '🍅 番茄计时器'

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.MINI_TITLE)
        self.root.geometry(f'{WIN_W}x{WIN_H}')
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DEEP)
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

        self.timer = PomodoroTimer(self.root)
        self.timer.on_tick = self._on_tick
        self.timer.on_finish = self._on_finish
        self.timer.on_mode_change = self._on_mode_change

        self.mute_var = tk.BooleanVar(value=False)
        self.topmost_var = tk.BooleanVar(value=False)

        self._mode_btns = {}
        self.tray_icon = None

        self._build_ui()
        self._center_window()
        self._refresh_display()
        self._update_action_button()
        self._setup_tray()

    # ================================================================
    #  UI 构建（三层卡片布局）
    # ================================================================
    def _build_ui(self):
        main = tk.Frame(self.root, bg=BG_DEEP)
        main.pack(fill='both', expand=True, padx=PADDING, pady=(PADDING, PADDING - 4))

        inner_w = WIN_W - 2 * PADDING  # 384px

        # ── 卡片一：模式切换栏 ──
        self._build_mode_bar(main, inner_w)

        # ── 卡片二：环形进度条 ──
        self._build_progress_card(main, inner_w)

        # ── 操作按钮 ──
        self.action_btn = RoundedButton(
            main, text='开 始',
            width=ACTION_BTN_W, height=ACTION_BTN_H, radius=ACTION_BTN_RADIUS,
            bg=BG_BUTTON, fg=TEXT_PRIMARY, hover_bg=BG_BUTTON_HOVER,
            font_spec=FONT_BUTTON_MAIN,
            command=self._toggle_start,
        )
        self.action_btn.pack(pady=(0, 8))

        self.reset_btn = RoundedButton(
            main, text='重 置',
            width=RESET_BTN_W, height=RESET_BTN_H, radius=RESET_BTN_RADIUS,
            bg=BG_BUTTON, fg=TEXT_SECONDARY, hover_bg=BG_BUTTON_HOVER,
            font_spec=FONT_BUTTON_MAIN,
            command=self._reset,
        )
        self.reset_btn.pack(pady=(0, 16))

        # ── 会话计数器 ──
        self.session_label = tk.Label(
            main, text='已完成 0 个番茄钟',
            font=FONT_SESSION, fg=TEXT_MUTED, bg=BG_DEEP,
        )
        self.session_label.pack()

        # 初始高亮
        self._highlight_mode(PomodoroTimer.WORK)

    # ── 模式切换栏（分段控件风格） ──
    def _build_mode_bar(self, parent, inner_w):
        """构建顶部分段控件式的模式切换栏。

        三个模式按钮置于共同的卡片 Canvas 之上，形成视觉整体。
        """
        card_h = MODE_BTN_H + 16  # 卡片高度
        bar_frame = tk.Frame(parent, bg=BG_DEEP, width=inner_w, height=card_h)
        bar_frame.pack(fill='x', pady=(0, 16))
        bar_frame.pack_propagate(False)

        # 卡片背景 Canvas（阴影 + 圆角表面）
        card_canvas = tk.Canvas(bar_frame, width=inner_w, height=card_h,
                                bg=BG_DEEP, highlightthickness=0)
        card_canvas.place(x=0, y=0)
        self._draw_card_bg(card_canvas, inner_w, card_h, radius=18)

        # 模式按钮（置于卡片上方）
        modes = [
            (PomodoroTimer.WORK, MODE_CONFIG[0]['btn_label']),
            (PomodoroTimer.SHORT_BREAK, MODE_CONFIG[1]['btn_label']),
            (PomodoroTimer.LONG_BREAK, MODE_CONFIG[2]['btn_label']),
        ]
        total_btns_w = (MODE_BTN_W * 3 + MODE_BTN_GAP * 2)
        start_x = (inner_w - total_btns_w) // 2

        for i, (mid, label) in enumerate(modes):
            color = MODE_CONFIG[mid]['color']
            btn = RoundedButton(
                bar_frame, text=label,
                width=MODE_BTN_W, height=MODE_BTN_H, radius=MODE_BTN_RADIUS,
                bg=BG_DEEP, fg=TEXT_SECONDARY, hover_bg='#2a2a3a',
                font_spec=FONT_BUTTON_MODE,
                command=lambda m=mid: self._switch_mode(m),
            )
            btn.place(x=start_x + i * (MODE_BTN_W + MODE_BTN_GAP),
                      y=(card_h - MODE_BTN_H) // 2)
            self._mode_btns[mid] = btn

        # 齿轮按钮（右侧）
        self.gear_btn = RoundedButton(
            bar_frame, text='⚙',
            width=GEAR_BTN_SIZE, height=GEAR_BTN_SIZE, radius=17,
            bg=BG_DEEP, fg=TEXT_MUTED, hover_bg='#2a2a3a',
            font_spec=(FONT_BUTTON_MODE[0], 14),
            command=self._open_settings,
        )
        self.gear_btn.place(x=inner_w - GEAR_BTN_SIZE - 8,
                            y=(card_h - GEAR_BTN_SIZE) // 2)

    # ── 进度环卡片 ──
    def _build_progress_card(self, parent, inner_w):
        """构建进度环卡片，包含阴影背景 + 环形进度条。"""
        card_h = RING_SIZE + 32
        card_frame = tk.Frame(parent, bg=BG_DEEP, width=inner_w, height=card_h)
        card_frame.pack(fill='x', pady=(0, 14))
        card_frame.pack_propagate(False)

        # 卡片背景 Canvas
        card_canvas = tk.Canvas(card_frame, width=inner_w, height=card_h,
                                bg=BG_DEEP, highlightthickness=0)
        card_canvas.place(x=0, y=0)
        self._draw_card_bg(card_canvas, inner_w, card_h, radius=20)

        # 环形进度条（置于卡片中央）
        self.ring = CircularProgressBar(card_frame, size=RING_SIZE,
                                        ring_width=RING_WIDTH)
        self.ring.place(relx=0.5, rely=0.5, anchor='center')

    @staticmethod
    def _draw_card_bg(canvas, w, h, radius):
        """在 Canvas 上绘制卡片背景（阴影 + 圆角表面）。

        阴影通过偏移的暗色圆角矩形实现。
        """
        r = radius
        d = 2 * r

        # 阴影（偏移 2px，半透明）
        def _round_rect(x1, y1, x2, y2, fill, outline=''):
            canvas.create_arc(x1, y1, x1 + d, y1 + d, start=90, extent=90,
                              style='pieslice', fill=fill, outline=outline)
            canvas.create_arc(x2 - d, y1, x2, y1 + d, start=0, extent=90,
                              style='pieslice', fill=fill, outline=outline)
            canvas.create_arc(x1, y2 - d, x1 + d, y2, start=180, extent=90,
                              style='pieslice', fill=fill, outline=outline)
            canvas.create_arc(x2 - d, y2 - d, x2, y2, start=270, extent=90,
                              style='pieslice', fill=fill, outline=outline)
            canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline=outline)
            canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline=outline)

        # 阴影
        _round_rect(2, 3, w, h + 1, fill=SHADOW)
        # 卡片表面
        _round_rect(0, 1, w - 2, h - 1, fill=BG_CARD)

    # ================================================================
    #  模式高亮
    # ================================================================
    def _highlight_mode(self, active_mode):
        """更新模式切换按钮的配色以反映当前模式"""
        for mid, btn in self._mode_btns.items():
            if mid == active_mode:
                c = MODE_CONFIG[mid]['color']
                h = MODE_CONFIG[mid]['hover']
                btn.set_colors(c, TEXT_ON_ACCENT, h)
            else:
                btn.set_colors(BG_DEEP, TEXT_SECONDARY, '#2a2a3a')

    # ================================================================
    #  设置窗口
    # ================================================================
    def _open_settings(self):
        SettingsWindow(self.root, self.timer, self.mute_var, self.topmost_var,
                       on_close_callback=self._on_settings_closed)

    def _on_settings_closed(self):
        if self.timer.state == PomodoroTimer.IDLE:
            self.timer.reset()
            self._refresh_display()
            self._highlight_mode(self.timer.mode)

    # ================================================================
    #  模式切换
    # ================================================================
    def _switch_mode(self, mode):
        self.timer.switch_mode(mode)
        self._highlight_mode(mode)
        self._refresh_display()
        self.ring.pulse()  # 模式切换脉冲动画

    # ================================================================
    #  计时器控制
    # ================================================================
    def _toggle_start(self):
        if self.timer.state == PomodoroTimer.RUNNING:
            self.timer.pause()
        else:
            self.timer.start()
        self._update_action_button()

    def _reset(self):
        self.timer.reset()
        self._highlight_mode(PomodoroTimer.WORK)
        self._update_action_button()
        self._refresh_display()
        self.ring.pulse()

    def _update_action_button(self):
        s = self.timer.state
        if s == PomodoroTimer.RUNNING:
            self.action_btn.set_text('暂 停')
            c = MODE_CONFIG[self.timer.mode]['color']
            h = MODE_CONFIG[self.timer.mode]['hover']
            self.action_btn.set_colors(c, TEXT_ON_ACCENT, h)
        elif s == PomodoroTimer.PAUSED:
            self.action_btn.set_text('继 续')
            c = MODE_CONFIG[self.timer.mode]['color']
            h = MODE_CONFIG[self.timer.mode]['hover']
            self.action_btn.set_colors(c, TEXT_ON_ACCENT, h)
        else:
            self.action_btn.set_text('开 始')
            self.action_btn.set_colors(BG_BUTTON, TEXT_PRIMARY, BG_BUTTON_HOVER)

    # ================================================================
    #  计时器回调
    # ================================================================
    def _on_tick(self, mins, secs, progress, mode):
        time_str = f'{mins:02d}:{secs:02d}'
        self.ring.set_value(progress * 100,
                            color=MODE_CONFIG[mode]['color'],
                            time_str=time_str,
                            mode_str=MODE_CONFIG[mode]['label'])
        self.root.title(f'{time_str} - {self.MINI_TITLE}')
        if self.tray_icon:
            self.tray_icon.title = f'{self.MINI_TITLE} {time_str}'

    def _on_finish(self, nxt_mode):
        self._update_action_button()
        if not self.mute_var.get():
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            self._show_window()
            from tkinter import messagebox
            messagebox.showinfo(
                '⏰ 时间到！',
                f'切换至：{MODE_CONFIG[nxt_mode]["label"]}',
            )
        self.ring.pulse()

    def _on_mode_change(self, mode):
        self._highlight_mode(mode)
        self.session_label.config(
            text=f'已完成 {self.timer.completed_sessions} 个番茄钟')
        m, s = divmod(self.timer.remaining, 60)
        self.ring.set_value(0, color=MODE_CONFIG[mode]['color'],
                            time_str=f'{m:02d}:{s:02d}',
                            mode_str=MODE_CONFIG[mode]['label'])
        self._update_action_button()

    def _refresh_display(self):
        m, s = divmod(self.timer.remaining, 60)
        self.ring.set_value(0, time_str=f'{m:02d}:{s:02d}',
                            mode_str=MODE_CONFIG[self.timer.mode]['label'])
        self.root.title(self.MINI_TITLE)
        if self.tray_icon:
            self.tray_icon.title = self.MINI_TITLE

    # ================================================================
    #  窗口辅助
    # ================================================================
    def _center_window(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - WIN_W) // 2
        y = (sh - WIN_H) // 2
        self.root.geometry(f'+{x}+{y}')

    # ================================================================
    #  系统托盘
    # ================================================================
    def _create_tray_image(self):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 60, 60], fill=TRAY_ICON_COLOR)
        return img

    def _setup_tray(self):
        menu = pystray.Menu(
            pystray.MenuItem('显示窗口', lambda: self.root.after(0, self._show_window)),
            pystray.MenuItem('开始 / 暂停', lambda: self.root.after(0, self._toggle_start)),
            pystray.MenuItem('重置', lambda: self.root.after(0, self._reset)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('退出', lambda: self.root.after(0, self._quit_app)),
        )
        self.tray_icon = pystray.Icon(
            'pomodoro', self._create_tray_image(), self.MINI_TITLE, menu)
        t = threading.Thread(target=self.tray_icon.run, daemon=True)
        t.start()

    def _show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def _on_close(self):
        self._quit_app()

    def _quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()

    # ================================================================
    #  启动
    # ================================================================
    def run(self):
        self.root.mainloop()
