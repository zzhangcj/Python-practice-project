# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A dark-themed Pomodoro timer desktop app built with Python Tkinter. Single file, no build system, no tests.

## Run

```bash
python pomodoro.py
```

## Architecture

`pomodoro.py` (613 lines) — four classes in a layered design:

| Class | Role |
|---|---|
| `RoundedButton(tk.Canvas)` | Reusable canvas-drawn rounded-rectangle button with hover/click handling |
| `CircularProgressBar(tk.Canvas)` | Ring progress arc showing remaining time, color-coded by mode |
| `PomodoroTimer` | Pure-logic timer state machine (no UI). **IDLE/RUNNING/PAUSED** states, **WORK/SHORT_BREAK/LONG_BREAK** modes. Uses `tk.after()` for 1-second ticks. Exposes callbacks: `.on_tick`, `.on_finish`, `.on_mode_change` |
| `PomodoroApp` | Main window that wires timer ↔ UI. Owns `PomodoroTimer`, builds all widgets, handles system tray via `pystray` |

Additional: `SettingsWindow` — Toplevel popup for duration config, mute, and always-on-top.

## Dependencies

- **tkinter** — bundled with Python on Windows
- **pystray** — system tray icon (`pip install pystray`)
- **Pillow** — tray icon drawing (`pip install Pillow`)
- **winsound** — bundled, for notification beeps (Windows only)

## Key behaviors

- Timer auto-advances: WORK → SHORT_BREAK (or LONG_BREAK every 4th session) → WORK → ...
- Closing the window minimizes to system tray instead of quitting; use tray menu "退出" to fully exit
- `PomodoroTimer` is independent of the UI — it fires callbacks that `PomodoroApp` binds to update widgets
