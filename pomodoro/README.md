# 番茄钟桌面应用｜个人学习项目
> 项目路径：C:\python实践\python_cursor_test
> 用途：Python tkinter GUI 实战 — 桌面番茄钟应用
> 笔记作者：自己
> 版本说明：单文件原型 → 多次 UI 迭代美化 → 模块化包结构重构

## 📌 一、项目简要介绍

这是一个基于 **Python tkinter** 的桌面番茄钟计时器，采用深色主题 + 环形进度条设计，支持系统托盘驻留。

### 学习方向

- **tkinter Canvas 自绘控件**：圆角按钮、环形进度条等原生 tkinter 不具备的 UI 组件
- **状态机模式**：Timer 纯逻辑层与 UI 层分离，通过回调解耦
- **系统托盘集成**：pystray + Pillow 实现最小化到托盘
- **Python 包结构**：从单文件逐步演进为 `pomodoro/` 标准包

### 核心功能

- 三种模式：专注（30分钟）/ 短休息（6分钟）/ 长休息（20分钟）
- 环形进度条实时显示倒计时，颜色随模式切换
- 每完成 4 轮专注自动触发长休息
- 自定义时长设置面板（齿轮按钮入口）
- 静音提醒 / 窗口置顶开关
- 关闭窗口最小化到系统托盘，托盘菜单控制
- 计时结束响铃 + 弹窗提示

---

## 📌 二、目录结构说明

```
python_cursor_test/
│
│  pomodoro.py                  # ← 向后兼容入口（旧版单文件调用）
│  CLAUDE.md                    # ← Claude Code 项目引导文件
│  chat.txt                     # ← Claude Code 完整对话记录（开发过程存档）
│
├── .claude/
│   ├── settings.local.json     # ← Claude Code 项目级权限配置（允许的 Bash 命令白名单 + 状态栏自定义）
│   ├── 要求文件                 # ← 项目需求占位文件（当前为空）
│   └── skills_frontend/
│       ├── SKILL.md            # ← 前端设计 Skill 定义（指导 Claude 生成个性化 UI 的风格规范）
│       └── LICENSE.txt         # ← Skill 随附的 Apache 2.0 开源协议
│
├── .idea/
│   ├── .gitignore              # ← PyCharm 忽略规则（排除 /shelf/ 和 workspace.xml）
│   ├── .name                   # ← PyCharm 项目显示名称（内容：pomodoro.py）
│   ├── misc.xml                # ← PyCharm 项目根配置（绑定 Python 3.13 SDK）
│   ├── modules.xml             # ← PyCharm 模块索引（指向 .iml 文件路径）
│   ├── python_cursor_test.iml  # ← PyCharm 模块定义（JDK 绑定 + 源码根目录声明）
│   ├── workspace.xml           # ← PyCharm 工作区状态（RunManager 配置、窗口布局、VCS 设置等）
│   └── inspectionProfiles/
│       └── profiles_settings.xml  # ← PyCharm 代码检查规则配置（当前使用默认规则）
│
├── __pycache__/
│   └── pomodoro.cpython-313.pyc   # ← Python 3.13 字节码缓存（由解释器自动生成）
│
└── pomodoro/                       # ← 核心包
    │
    ├── __init__.py                 # ← 包标识文件（空文件，标记为 Python 包）
    ├── __main__.py                 # ← 允许通过 `python -m pomodoro` 启动应用
    ├── main.py                     # ← 程序入口层：run() 函数，实例化 PomodoroApp 并启动主循环
    ├── app.py                      # ← 主窗口层：组装全部 UI 组件、连线计时器回调、管理系统托盘
    ├── timer.py                    # ← 计时逻辑层：纯状态机（IDLE/RUNNING/PAUSED），与 UI 零耦合
    ├── constants.py                # ← 全局常量层：颜色、字体、尺寸、动画参数、模式配置集中管理
    ├── settings.py                 # ← 设置弹窗：自定义三种模式时长、静音/置顶复选框、保存/取消按钮
    │
    └── widgets/                    # ← 自定义控件包
        ├── __init__.py             # ← 包标识文件（空文件）
        ├── rounded_button.py       # ← 圆角按钮控件（Canvas 绘制，支持 hover 颜色动画 + 点击缩放反馈）
        └── circular_progress.py    # ← 环形进度条控件（Canvas 绘制弧线，支持指数衰减动画 + 脉冲效果）
```

### 逐文件说明

#### 根目录

| 文件 | 类型 | 作用 |
|------|------|------|
| `pomodoro.py` | Python | 向后兼容入口，内部 `from pomodoro.main import run` 转发调用，保证旧命令 `python pomodoro.py` 仍可用 |
| `CLAUDE.md` | Markdown | Claude Code 项目引导文件，描述项目架构、依赖、运行方式、关键行为，AI 助手据此理解项目 |
| `chat.txt` | 文本 | 完整 Claude Code 对话转录（约 2700 行），记录从零搭建到多轮迭代的全部过程，可作学习参考 |

#### `.claude/` 目录 — Claude Code 配置

| 文件 | 作用 |
|------|------|
| `settings.local.json` | 项目级权限白名单（允许特定 Bash 命令免确认执行）及自定义终端状态栏格式 |
| `要求文件` | 空占位文件，本意为存放原始需求描述，当前未启用 |
| `skills_frontend/SKILL.md` | 前端设计 Skill 定义文件，指导 Claude 在生成 UI 时遵循个性化设计规范（配色、字体、排版），避免模板化样式 |
| `skills_frontend/LICENSE.txt` | Apache 2.0 开源许可证全文，仅约束此 Skill 文件本身的使用 |

#### `.idea/` 目录 — PyCharm IDE 配置

| 文件 | 作用 |
|------|------|
| `.gitignore` | 告知 Git 忽略 IDE 自动生成的 `/shelf/` 目录和 `workspace.xml`（不过本仓库当前未纳入 Git 管理） |
| `.name` | 记录 PyCharm 项目显示名称为 `pomodoro.py` |
| `misc.xml` | 绑定项目级别的 Python 解释器（Python 3.13 SDK），PyCharm 据此提供代码补全和语法检查 |
| `modules.xml` | 声明项目的模块组成，指向 `python_cursor_test.iml` 模块定义文件 |
| `python_cursor_test.iml` | 模块核心定义：源码根目录 `$MODULE_DIR$`、JDK 类型为 Python SDK、源码文件夹标记 |
| `workspace.xml` | 工作区运行时状态：RunManager 中的 `pomodoro` 运行配置（脚本路径、环境变量 `PYTHONUNBUFFERED=1`）、VCS 变更列表、窗口视图状态等 |
| `inspectionProfiles/profiles_settings.xml` | 代码检查配置文件（当前使用 PyCharm 默认规则，未定制） |

#### `__pycache__/` 目录

Python 解释器自动生成的字节码缓存目录。`.pyc` 文件是源码编译后的中间表示，用于加速模块导入。**不应手动编辑或提交到版本控制**（建议在 `.gitignore` 中添加 `__pycache__/`）。

#### `pomodoro/` 包 — 核心代码

| 文件 | 所属层 | 职责 |
|------|--------|------|
| `__init__.py` | 包标识 | 空文件，将普通文件夹标记为 Python 可导入的「包」 |
| `__main__.py` | 入口层 | 支持 `python -m pomodoro` 方式启动，调用 `main.run()` |
| `main.py` | 入口层 | `run()` 函数创建 `PomodoroApp` 实例并启动 `mainloop()`，是推荐的启动入口 |
| `app.py` | 主窗口层 | 组装全部 UI（模式切换栏 / 环形进度条 / 操作按钮 / 会话计数）、绑定 `PomodoroTimer` 回调、管理系统托盘和设置窗口 |
| `timer.py` | 计时逻辑层 | 纯状态机 `PomodoroTimer`：维护 IDLE→RUNNING↔PAUSED 三种状态、WORK/SHORT_BREAK/LONG_BREAK 三种模式，通过 `on_tick` / `on_finish` / `on_mode_change` 回调与 UI 通信，不包含任何 tkinter 控件代码 |
| `constants.py` | 常量配置层 | 集中存放全部视觉参数：4 级深度颜色（BG_DEEP → SHADOW）、模式配色字典 `MODE_CONFIG`、字体规格、窗口/控件尺寸、动画参数（帧率/衰减系数/脉冲时长）、默认时长和长休息触发间隔 |
| `settings.py` | 设置弹窗 | `SettingsWindow` 类：Toplevel 弹窗，包含三个时长输入框、静音/置顶复选框、保存/取消按钮；保存时校验正整数输入并更新 Timer 时长 |

#### `pomodoro/widgets/` 子包 — 自定义控件

| 文件 | 控件 | 技术要点 |
|------|------|----------|
| `__init__.py` | 包标识 | 空文件 |
| `rounded_button.py` | `RoundedButton(tk.Canvas)` | Canvas 自绘圆角矩形按钮：四个弧形角 + 两个中心矩形拼合；hover 时 RGB 指数衰减颜色过渡；点击时 2px 缩放反馈；上半部提亮 8% 模拟顶光源渐变 |
| `circular_progress.py` | `CircularProgressBar(tk.Canvas)` | Canvas 自绘环形进度条：暗色轨道弧 + 彩色进度弧 + 进度发光层 + 阴影偏移；`set_value()` 触发指数衰减动画（`PROGRESS_DECAY=0.15`）平滑过渡；`pulse()` 方法提供模式切换时的环宽脉冲效果 |

---

## 📌 三、依赖与运行方式

### 依赖安装

```bash
pip install pystray pillow
```

> 其余依赖（`tkinter`、`winsound`、`threading`）均为 Python 标准库，无需额外安装。

### 启动方式（三选一）

```bash
# 方式一：模块方式启动（推荐）
python -m pomodoro

# 方式二：直接运行入口文件
python pomodoro/main.py

# 方式三：向后兼容入口
python pomodoro.py
```

### 关闭应用

- 点击窗口关闭按钮 → **最小化到系统托盘**（不退出）
- 右键系统托盘红色图标 → 选择「退出」→ 彻底关闭

---

## 📌 四、架构设计

### 分层架构

```
pomodoro/main.py          ← 入口层：创建 App 实例
pomodoro/app.py           ← 主窗口层：UI 组装 + 回调绑定
pomodoro/timer.py         ← 逻辑层：纯状态机（与 UI 零耦合）
pomodoro/settings.py      ← 设置层：Toplevel 弹窗
pomodoro/constants.py     ← 常量层：颜色/字体/尺寸/动画参数
pomodoro/widgets/*.py     ← 控件层：Canvas 自绘组件
```

### 数据流

```
用户点击按钮
    ↓
PomodoroApp._toggle_start()
    ↓
PomodoroTimer.start() / pause()
    ↓ (每 1 秒 tick)
PomodoroTimer.on_tick(mins, secs, progress, mode)
    ↓
PomodoroApp._on_tick() → 更新 ring.set_value() + 窗口标题 + 托盘标题
```

### 状态机

```
         ┌──────────────────────────┐
         │                          │
         ▼                          │
     ┌──────┐   start()   ┌─────────┐   pause()   ┌────────┐
     │ IDLE │ ──────────→ │ RUNNING │ ──────────→ │ PAUSED │
     └──────┘             └─────────┘ ←────────── └────────┘
         ▲                     │        start()
         │     reset()         │ remaining ≤ 0
         └─────────────────────┘
                               │
                               ▼
                          _finish()
                    自动切换下一模式
               WORK → BREAK → WORK → ...
```

---

## 📌 五、踩坑记录 & 个人理解

> 此处自由记录学习过程中遇到的疑难问题和解决思路。

1. **tkinter Canvas `create_arc` 的 `outline` 参数重复传递**：在 `_round_rect()` 方法中同时通过 `**kw` 传递和显式写 `outline=''` 会导致 `TypeError: got multiple values for keyword argument 'outline'`。解决：统一通过 `**kw` 传递，不在调用处写死。

2. **Canvas 实例属性名与 Tcl 内部属性冲突**：自定义 `SimpleProgressBar(tk.Canvas)` 中用了 `self._w` 作为宽度变量名，但 `tk.Canvas` 内部已有 `_w` 属性指向 Tcl 路径，导致运行时崩溃。解决：改为 `self._bar_w` / `self._bar_h` 避免覆盖基类属性。

3. **`RoundedButton` 构造函数的 `bg` 参数**：`tk.Canvas.__init__` 本身接受 `bg` 关键字，若子类 `RoundedButton.__init__` 也定义 `bg` 参数并直接转发给 `super().__init__`，行为正常；但需注意当外部调用也传 `bg` 时的优先级问题 — 当前代码中已通过 `kw.pop('bg')` 做了防御处理。
