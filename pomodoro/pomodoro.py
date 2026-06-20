import tkinter as tk
from tkinter import ttk, messagebox
import threading
import winsound
from PIL import Image, ImageDraw
import pystray


# ============================================================
#  Rounded-rectangle Canvas button
# ============================================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, width=100, height=36, radius=18,
                 bg='#2e2e3e', fg='#ffffff', hover_bg=None,
                 command=None, font_size=12, **kw):
        super().__init__(parent, width=width, height=height,
                         bg='#1e1e2e', highlightthickness=0, **kw)
        self._btn_w = width
        self._btn_h = height
        self._btn_r = min(radius, height // 2)
        self._text = text
        self._bg = bg
        self._fg = fg
        self._hover_bg = hover_bg or bg
        self._command = command
        self._font_size = font_size
        self._hovered = False

        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        self._draw()

    def set_colors(self, bg, fg, hover_bg=None):
        self._bg = bg
        self._fg = fg
        if hover_bg is not None:
            self._hover_bg = hover_bg
        self._draw()

    def set_text(self, text):
        self._text = text
        self._draw()

    def _draw(self):
        self.delete('all')
        bg = self._hover_bg if self._hovered else self._bg
        self._round_rect(0, 0, self._btn_w, self._btn_h, self._btn_r, fill=bg, outline='')
        self.create_text(self._btn_w // 2, self._btn_h // 2, text=self._text, fill=self._fg,
                         font=('Microsoft YaHei UI', self._font_size, 'bold'))

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
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

    def _on_enter(self, e):
        self._hovered = True
        self._draw()

    def _on_leave(self, e):
        self._hovered = False
        self._draw()

    def _on_click(self, e):
        if self._command:
            self._command()


# ============================================================
#  Circular ring progress bar (Canvas)
# ============================================================
class CircularProgressBar(tk.Canvas):
    def __init__(self, parent, size=260, ring_width=16, **kw):
        super().__init__(parent, width=size, height=size,
                         bg='#1e1e2e', highlightthickness=0, **kw)
        self._size = size
        self._cx = size // 2
        self._cy = size // 2
        self._mid_r = (size // 2) - 8       # arc midline radius
        self._width = ring_width
        self._val = 0          # 0 – 100
        self._color = '#E74C3C'
        self._time_str = '30:00'
        self._mode_str = '专注时间'

    def set_value(self, percent, color=None, time_str=None, mode_str=None):
        self._val = max(0, min(100, percent))
        if color is not None:
            self._color = color
        if time_str is not None:
            self._time_str = time_str
        if mode_str is not None:
            self._mode_str = mode_str
        self._redraw()

    def _redraw(self):
        self.delete('all')
        # bounding square for arc
        d = 2 * self._mid_r
        x1 = self._cx - self._mid_r
        y1 = self._cy - self._mid_r
        x2 = self._cx + self._mid_r
        y2 = self._cy + self._mid_r

        # background ring (dark track)
        self.create_arc(x1, y1, x2, y2, start=90, extent=-360,
                        style='arc', width=self._width,
                        outline='#2a2a3a')

        # progress arc (coloured, clockwise from top)
        extent = -self._val * 360 / 100
        if abs(extent) > 0.5:
            self.create_arc(x1, y1, x2, y2, start=90, extent=extent,
                            style='arc', width=self._width,
                            outline=self._color)

        # centre time
        self.create_text(self._cx, self._cy - 6, text=self._time_str,
                         fill='#ffffff',
                         font=('Microsoft YaHei UI', 38, 'bold'))

        # mode label below time
        self.create_text(self._cx, self._cy + 28, text=self._mode_str,
                         fill='#888888',
                         font=('Microsoft YaHei UI', 12))


# ============================================================
#  Settings popup window
# ============================================================
class SettingsWindow:
    def __init__(self, parent, timer, mute_var, topmost_var, on_close_callback):
        self._timer = timer
        self._mute_var = mute_var
        self._topmost_var = topmost_var
        self._on_close = on_close_callback

        self.win = tk.Toplevel(parent)
        self.win.title('设置')
        self.win.geometry('320x280')
        self.win.resizable(False, False)
        self.win.configure(bg='#1e1e2e')
        self.win.transient(parent)
        self.win.protocol('WM_DELETE_WINDOW', self._close)

        self._build()
        self._center(parent)

    def _build(self):
        fr = tk.Frame(self.win, bg='#1e1e2e')
        fr.pack(fill='both', expand=True, padx=24, pady=20)

        # ---- duration inputs ----
        lbl = tk.Label(fr, text='自定义时长（分钟）', font=('Microsoft YaHei UI', 12, 'bold'),
                       fg='#cccccc', bg='#1e1e2e')
        lbl.pack(anchor='w', pady=(0, 12))

        rows = tk.Frame(fr, bg='#1e1e2e')
        rows.pack(fill='x', pady=(0, 14))
        for i, (label, var, default) in enumerate([
            ('专注时长', 'work_var', 30),
            ('短时休息', 'short_var', 6),
            ('长时休息', 'long_var', 20),
        ]):
            row = tk.Frame(rows, bg='#1e1e2e')
            row.pack(fill='x', pady=3)
            tk.Label(row, text=label, font=('Microsoft YaHei UI', 11),
                     fg='#aaaaaa', bg='#1e1e2e', width=10, anchor='w').pack(side='left')
            sv = tk.StringVar(value=str(default))
            setattr(self, label, sv)  # store for later
            setattr(self, var, sv)    # e.g. self.work_var
            e = tk.Entry(row, textvariable=sv, width=8, justify='center',
                         font=('Microsoft YaHei UI', 11),
                         bg='#2e2e3e', fg='#ffffff', insertbackground='#ffffff',
                         relief='flat', bd=0,
                         highlightbackground='#3e3e4e', highlightthickness=1)
            e.pack(side='left', ipady=3)

        # ---- checkboxes ----
        chk_fr = tk.Frame(fr, bg='#1e1e2e')
        chk_fr.pack(fill='x', pady=(0, 16))
        tk.Checkbutton(chk_fr, text='静音提醒', variable=self._mute_var,
                       bg='#1e1e2e', fg='#cccccc', selectcolor='#2e2e3e',
                       activebackground='#1e1e2e', activeforeground='#ffffff',
                       font=('Microsoft YaHei UI', 11),
                       ).pack(side='left', padx=(0, 20))
        tk.Checkbutton(chk_fr, text='窗口置顶', variable=self._topmost_var,
                       bg='#1e1e2e', fg='#cccccc', selectcolor='#2e2e3e',
                       activebackground='#1e1e2e', activeforeground='#ffffff',
                       font=('Microsoft YaHei UI', 11),
                       ).pack(side='left')

        # ---- buttons ----
        btn_fr = tk.Frame(fr, bg='#1e1e2e')
        btn_fr.pack(fill='x')
        RoundedButton(btn_fr, text='保存', width=120, height=34, radius=17,
                      bg='#3498db', fg='#ffffff', hover_bg='#2980b9',
                      font_size=12, command=self._save).pack(side='left', padx=(0, 12))
        RoundedButton(btn_fr, text='取消', width=120, height=34, radius=17,
                      bg='#3e3e4e', fg='#aaaaaa', hover_bg='#4e4e5e',
                      font_size=12, command=self._close).pack(side='left')

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


# ============================================================
#  Core timer logic (unchanged except one helper)
# ============================================================
class PomodoroTimer:
    IDLE, RUNNING, PAUSED = 0, 1, 2
    WORK, SHORT_BREAK, LONG_BREAK = 0, 1, 2

    MODE_LABELS = {
        WORK: '专注时间',
        SHORT_BREAK: '短时休息',
        LONG_BREAK: '长时休息',
    }
    MODE_COLORS = {
        WORK: '#E74C3C',
        SHORT_BREAK: '#27AE60',
        LONG_BREAK: '#3498DB',
    }
    # hover variants for buttons
    MODE_HOVER = {
        WORK: '#c0392b',
        SHORT_BREAK: '#219a52',
        LONG_BREAK: '#2980b9',
    }

    def __init__(self, root):
        self._root = root
        self.durations = {
            self.WORK: 30 * 60,
            self.SHORT_BREAK: 6 * 60,
            self.LONG_BREAK: 20 * 60,
        }
        self.state = self.IDLE
        self.mode = self.WORK
        self.remaining = self.durations[self.WORK]
        self.total = self.durations[self.WORK]
        self.session = 0
        self._job_id = None

        self.on_tick = None
        self.on_finish = None
        self.on_mode_change = None

    @property
    def progress(self):
        if self.total <= 0:
            return 0
        return (self.total - self.remaining) / self.total

    @property
    def completed_sessions(self):
        return self.session

    def set_duration(self, mode, minutes):
        self.durations[mode] = max(1, int(minutes)) * 60

    def switch_mode(self, mode):
        """Manually switch to a mode and reset to idle (for UI mode toggles)."""
        self.pause()
        self.state = self.IDLE
        self.mode = mode
        self.remaining = self.durations[mode]
        self.total = self.durations[mode]
        self._notify_tick()
        if self.on_mode_change:
            self.on_mode_change(mode)

    def start(self):
        if self.state == self.IDLE:
            self.remaining = self.durations[self.mode]
            self.total = self.remaining
        self.state = self.RUNNING
        self._tick()

    def pause(self):
        if self.state != self.RUNNING:
            return
        self.state = self.PAUSED
        if self._job_id is not None:
            self._root.after_cancel(self._job_id)
            self._job_id = None

    def reset(self):
        self.pause()
        self.state = self.IDLE
        self.mode = self.WORK
        self.session = 0
        self.remaining = self.durations[self.WORK]
        self.total = self.durations[self.WORK]
        self._notify_tick()
        if self.on_mode_change:
            self.on_mode_change(self.mode)

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
        self.state = self.IDLE
        self._job_id = None
        if self.mode == self.WORK:
            self.session += 1
            nxt = self.LONG_BREAK if self.session % 4 == 0 else self.SHORT_BREAK
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


# ============================================================
#  Main application — dark themed UI
# ============================================================
class PomodoroApp:
    WIN_W = 400
    WIN_H = 500
    BG = '#1e1e2e'

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('🍅 番茄计时器')
        self.root.geometry(f'{self.WIN_W}x{self.WIN_H}')
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)
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

    # ---- UI construction ----
    def _build_ui(self):
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill='both', expand=True, padx=24, pady=(20, 16))

        # ---- top bar: mode toggles + gear ----
        top_bar = tk.Frame(main, bg=self.BG)
        top_bar.pack(fill='x', pady=(0, 14))

        mode_frame = tk.Frame(top_bar, bg=self.BG)
        mode_frame.pack(expand=True)

        modes = [
            (PomodoroTimer.WORK, '专注'),
            (PomodoroTimer.SHORT_BREAK, '短休息'),
            (PomodoroTimer.LONG_BREAK, '长休息'),
        ]
        for mid, label in modes:
            color = PomodoroTimer.MODE_COLORS[mid]
            btn = RoundedButton(mode_frame, text=label, width=82, height=32, radius=16,
                                bg=self.BG, fg='#aaaaaa', hover_bg='#2a2a3a',
                                font_size=11,
                                command=lambda m=mid: self._switch_mode(m))
            btn.pack(side='left', padx=3)
            self._mode_btns[mid] = btn

        # gear settings button (top-right corner)
        self.gear_btn = RoundedButton(top_bar, text='⚙', width=32, height=32, radius=16,
                                      bg=self.BG, fg='#888888', hover_bg='#2a2a3a',
                                      font_size=16, command=self._open_settings)
        self.gear_btn.place(relx=1.0, rely=0.5, anchor='e')

        # ---- circular ring progress ----
        self.ring = CircularProgressBar(main, size=260, ring_width=16)
        self.ring.pack(pady=(0, 12))

        # ---- action buttons ----
        btn_area = tk.Frame(main, bg=self.BG)
        btn_area.pack(fill='x', pady=(0, 8))

        self.action_btn = RoundedButton(btn_area, text='开 始', width=340, height=44,
                                        radius=22, bg='#2a2a3a', fg='#ffffff',
                                        hover_bg='#3a3a4a', font_size=14,
                                        command=self._toggle_start)
        self.action_btn.pack(pady=(0, 8))

        self.reset_btn = RoundedButton(btn_area, text='重 置', width=340, height=44,
                                       radius=22, bg='#2a2a3a', fg='#aaaaaa',
                                       hover_bg='#3a3a4a', font_size=14,
                                       command=self._reset)
        self.reset_btn.pack()

        # ---- session counter ----
        self.session_label = tk.Label(main, text='已完成 0 个番茄钟',
                                      font=('Microsoft YaHei UI', 12),
                                      fg='#666666', bg=self.BG)
        self.session_label.pack(pady=(14, 0))

        # initial highlight
        self._highlight_mode(PomodoroTimer.WORK)

    def _highlight_mode(self, active_mode):
        """Update mode-toggle button colours."""
        for mid, btn in self._mode_btns.items():
            if mid == active_mode:
                c = PomodoroTimer.MODE_COLORS[mid]
                h = PomodoroTimer.MODE_HOVER[mid]
                btn.set_colors(c, '#ffffff', h)
            else:
                btn.set_colors(self.BG, '#aaaaaa', '#2a2a3a')

    # ---- open settings popup ----
    def _open_settings(self):
        SettingsWindow(self.root, self.timer, self.mute_var, self.topmost_var,
                       on_close_callback=self._on_settings_closed)

    def _on_settings_closed(self):
        if self.timer.state == PomodoroTimer.IDLE:
            self.timer.reset()
            self._refresh_display()
            self._highlight_mode(self.timer.mode)

    # ---- mode toggle ----
    def _switch_mode(self, mode):
        self.timer.switch_mode(mode)
        self._highlight_mode(mode)
        self._refresh_display()

    # ---- timer controls ----
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

    def _update_action_button(self):
        s = self.timer.state
        if s == PomodoroTimer.RUNNING:
            self.action_btn.set_text('暂 停')
            # Set to current mode colour
            c = PomodoroTimer.MODE_COLORS[self.timer.mode]
            h = PomodoroTimer.MODE_HOVER[self.timer.mode]
            self.action_btn.set_colors(c, '#ffffff', h)
        elif s == PomodoroTimer.PAUSED:
            self.action_btn.set_text('继 续')
            c = PomodoroTimer.MODE_COLORS[self.timer.mode]
            h = PomodoroTimer.MODE_HOVER[self.timer.mode]
            self.action_btn.set_colors(c, '#ffffff', h)
        else:
            self.action_btn.set_text('开 始')
            self.action_btn.set_colors('#2a2a3a', '#ffffff', '#3a3a4a')

    # ---- Timer callbacks ----
    def _on_tick(self, mins, secs, progress, mode):
        time_str = f'{mins:02d}:{secs:02d}'
        self.ring.set_value(progress * 100,
                            color=PomodoroTimer.MODE_COLORS[mode],
                            time_str=time_str,
                            mode_str=PomodoroTimer.MODE_LABELS[mode])
        self.root.title(f'{time_str} - 🍅 番茄计时器')
        if self.tray_icon:
            self.tray_icon.title = f'🍅 番茄计时器 {time_str}'

    def _on_finish(self, nxt_mode):
        self._update_action_button()
        if not self.mute_var.get():
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            self._show_window()
            messagebox.showinfo(
                '⏰ 时间到！',
                f'切换至：{PomodoroTimer.MODE_LABELS[nxt_mode]}',
            )

    def _on_mode_change(self, mode):
        self._highlight_mode(mode)
        self.session_label.config(
            text=f'已完成 {self.timer.completed_sessions} 个番茄钟')
        m, s = divmod(self.timer.remaining, 60)
        self.ring.set_value(0, color=PomodoroTimer.MODE_COLORS[mode],
                            time_str=f'{m:02d}:{s:02d}',
                            mode_str=PomodoroTimer.MODE_LABELS[mode])
        self._update_action_button()

    def _refresh_display(self):
        m, s = divmod(self.timer.remaining, 60)
        self.ring.set_value(0, time_str=f'{m:02d}:{s:02d}',
                            mode_str=PomodoroTimer.MODE_LABELS[self.timer.mode])
        self.root.title('🍅 番茄计时器')
        if self.tray_icon:
            self.tray_icon.title = '🍅 番茄计时器'

    # ---- Window helpers ----
    def _center_window(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - self.WIN_W) // 2
        y = (sh - self.WIN_H) // 2
        self.root.geometry(f'+{x}+{y}')

    def _toggle_topmost(self):
        self.root.attributes('-topmost', self.topmost_var.get())

    # ---- System tray ----
    def _create_tray_image(self):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 60, 60], fill='#E74C3C')
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
            'pomodoro', self._create_tray_image(), '🍅 番茄计时器', menu)
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

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    PomodoroApp().run()
