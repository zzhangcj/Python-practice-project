"""设置弹窗。

允许自定义三种模式的时长（分钟）、静音提醒、窗口置顶。
"""

import tkinter as tk
from tkinter import messagebox
from pomodoro.constants import (
    BG_DEEP, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_ON_ACCENT,
    SETTINGS_ENTRY_BG, SETTINGS_ENTRY_BORDER,
    SETTINGS_SAVE_BG, SETTINGS_SAVE_HOVER,
    SETTINGS_CANCEL_BG, SETTINGS_CANCEL_HOVER,
    FONT_SETTINGS_TITLE, FONT_SETTINGS_LABEL, FONT_SETTINGS_ENTRY,
    FONT_SETTINGS_CHECK, FONT_SETTINGS_BTN,
    SETTINGS_WIN_W, SETTINGS_WIN_H,
)
from pomodoro.widgets.rounded_button import RoundedButton


class SettingsWindow:
    """设置弹窗（Toplevel）。

    包含三个时长输入框、静音/置顶复选框、保存/取消按钮。
    """

    def __init__(self, parent, timer, mute_var, topmost_var, on_close_callback):
        self._timer = timer
        self._mute_var = mute_var
        self._topmost_var = topmost_var
        self._on_close = on_close_callback

        self.win = tk.Toplevel(parent)
        self.win.title('设置')
        self.win.geometry(f'{SETTINGS_WIN_W}x{SETTINGS_WIN_H}')
        self.win.resizable(False, False)
        self.win.configure(bg=BG_DEEP)
        self.win.transient(parent)
        self.win.protocol('WM_DELETE_WINDOW', self._close)

        self._build()
        self._center(parent)

    def _build(self):
        fr = tk.Frame(self.win, bg=BG_DEEP)
        fr.pack(fill='both', expand=True, padx=24, pady=20)

        # ---- 标题 ----
        lbl = tk.Label(fr, text='自定义时长（分钟）',
                       font=FONT_SETTINGS_TITLE,
                       fg=TEXT_PRIMARY, bg=BG_DEEP)
        lbl.pack(anchor='w', pady=(0, 12))

        # ---- 时长输入 ----
        rows = tk.Frame(fr, bg=BG_DEEP)
        rows.pack(fill='x', pady=(0, 14))
        for label, var_name, default in [
            ('专注时长', 'work_var', 30),
            ('短时休息', 'short_var', 6),
            ('长时休息', 'long_var', 20),
        ]:
            row = tk.Frame(rows, bg=BG_DEEP)
            row.pack(fill='x', pady=3)
            tk.Label(row, text=label, font=FONT_SETTINGS_LABEL,
                     fg=TEXT_SECONDARY, bg=BG_DEEP,
                     width=10, anchor='w').pack(side='left')
            sv = tk.StringVar(value=str(default))
            setattr(self, var_name, sv)
            e = tk.Entry(row, textvariable=sv, width=8, justify='center',
                         font=FONT_SETTINGS_ENTRY,
                         bg=SETTINGS_ENTRY_BG, fg=TEXT_PRIMARY,
                         insertbackground=TEXT_PRIMARY,
                         relief='flat', bd=0,
                         highlightbackground=SETTINGS_ENTRY_BORDER,
                         highlightthickness=1)
            e.pack(side='left', ipady=3)

        # ---- 复选框 ----
        chk_fr = tk.Frame(fr, bg=BG_DEEP)
        chk_fr.pack(fill='x', pady=(0, 16))
        tk.Checkbutton(chk_fr, text='静音提醒', variable=self._mute_var,
                       bg=BG_DEEP, fg=TEXT_PRIMARY, selectcolor='#2e2e3e',
                       activebackground=BG_DEEP, activeforeground=TEXT_PRIMARY,
                       font=FONT_SETTINGS_CHECK,
                       ).pack(side='left', padx=(0, 20))
        tk.Checkbutton(chk_fr, text='窗口置顶', variable=self._topmost_var,
                       bg=BG_DEEP, fg=TEXT_PRIMARY, selectcolor='#2e2e3e',
                       activebackground=BG_DEEP, activeforeground=TEXT_PRIMARY,
                       font=FONT_SETTINGS_CHECK,
                       ).pack(side='left')

        # ---- 按钮 ----
        btn_fr = tk.Frame(fr, bg=BG_DEEP)
        btn_fr.pack(fill='x')
        RoundedButton(btn_fr, text='保存', width=120, height=34, radius=17,
                      bg=SETTINGS_SAVE_BG, fg=TEXT_ON_ACCENT,
                      hover_bg=SETTINGS_SAVE_HOVER,
                      font_spec=FONT_SETTINGS_BTN,
                      command=self._save).pack(side='left', padx=(0, 12))
        RoundedButton(btn_fr, text='取消', width=120, height=34, radius=17,
                      bg=SETTINGS_CANCEL_BG, fg=TEXT_SECONDARY,
                      hover_bg=SETTINGS_CANCEL_HOVER,
                      font_spec=FONT_SETTINGS_BTN,
                      command=self._close).pack(side='left')

    def _save(self):
        try:
            w = int(self.work_var.get())
            s = int(self.short_var.get())
            l = int(self.long_var.get())
            if w < 1 or s < 1 or l < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning('输入无效', '请输入正整数（分钟）。')
            return
        self._timer.set_duration(self._timer.WORK, w)
        self._timer.set_duration(self._timer.SHORT_BREAK, s)
        self._timer.set_duration(self._timer.LONG_BREAK, l)
        self._close()
        if self._on_close:
            self._on_close()

    def _close(self):
        self.win.destroy()

    def _center(self, parent):
        self.win.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        w = self.win.winfo_width()
        h = self.win.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.win.geometry(f'+{x}+{y}')
        self.win.grab_set()
