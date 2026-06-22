"""番茄钟应用全局常量：颜色、字体、尺寸、动画参数。

所有视觉相关的"魔法数字"集中在此，方便统一调整主题。
"""

# ============================================================
#  颜色层级（从深到浅）
# ============================================================
BG_DEEP = '#1a1a2e'          # 窗口背景
BG_CARD = '#252545'          # 卡片 / 抬升表面
BG_BUTTON = '#2e2e50'        # 默认按钮底色
BG_BUTTON_HOVER = '#3d3d62'  # 默认按钮悬停
RING_TRACK = '#2d2d4a'       # 进度条轨道
SHADOW = '#12122a'            # 卡片阴影色（比卡片更深）

# ---- 文字 ----
TEXT_PRIMARY = '#e8e8f0'
TEXT_SECONDARY = '#8888aa'
TEXT_MUTED = '#5a5a7a'
TEXT_ON_ACCENT = '#ffffff'

# ---- 设置窗口 ----
SETTINGS_ENTRY_BG = '#2e2e3e'
SETTINGS_ENTRY_BORDER = '#3e3e4e'
SETTINGS_SAVE_BG = '#3498db'
SETTINGS_SAVE_HOVER = '#2980b9'
SETTINGS_CANCEL_BG = '#3e3e4e'
SETTINGS_CANCEL_HOVER = '#4e4e5e'

# ---- 系统托盘 ----
TRAY_ICON_COLOR = '#E74C3C'

# ============================================================
#  模式配色
# ============================================================
MODE_CONFIG = {
    0: {  # WORK（专注）
        'color': '#ff6b6b',
        'hover': '#ee5a5a',
        'glow': '#cc5555',
        'label': '专注时间',
        'btn_label': '专注',
    },
    1: {  # SHORT_BREAK（短休）
        'color': '#51cf66',
        'hover': '#40c057',
        'glow': '#3da64f',
        'label': '短时休息',
        'btn_label': '短休息',
    },
    2: {  # LONG_BREAK（长休）
        'color': '#5c7cfa',
        'hover': '#4c6ef5',
        'glow': '#495ec8',
        'label': '长时休息',
        'btn_label': '长休息',
    },
}

# ============================================================
#  字体
# ============================================================
FONT_FAMILY = 'Microsoft YaHei UI'
FONT_TIME = (FONT_FAMILY, 44, 'bold')
FONT_MODE_LABEL = (FONT_FAMILY, 13)
FONT_BUTTON_MAIN = (FONT_FAMILY, 13, 'bold')
FONT_BUTTON_MODE = (FONT_FAMILY, 11, 'bold')
FONT_SESSION = (FONT_FAMILY, 12)
FONT_SETTINGS_TITLE = (FONT_FAMILY, 12, 'bold')
FONT_SETTINGS_LABEL = (FONT_FAMILY, 11)
FONT_SETTINGS_ENTRY = (FONT_FAMILY, 11)
FONT_SETTINGS_CHECK = (FONT_FAMILY, 11)
FONT_SETTINGS_BTN = (FONT_FAMILY, 12)

# ============================================================
#  窗口与部件尺寸
# ============================================================
WIN_W = 440
WIN_H = 580
PADDING = 28

# 环形进度条
RING_SIZE = 280
RING_WIDTH = 18

# 模式切换按钮
MODE_BTN_W = 88
MODE_BTN_H = 34
MODE_BTN_RADIUS = 17
MODE_BTN_GAP = 4

# 齿轮按钮
GEAR_BTN_SIZE = 34

# 操作按钮
ACTION_BTN_W = 360
ACTION_BTN_H = 48
ACTION_BTN_RADIUS = 24
RESET_BTN_W = 360
RESET_BTN_H = 42
RESET_BTN_RADIUS = 21

# 会话计数药丸
SESSION_PILL_W = 220
SESSION_PILL_H = 32

# 设置窗口
SETTINGS_WIN_W = 340
SETTINGS_WIN_H = 300

# ============================================================
#  动画参数（毫秒）
# ============================================================
ANIM_FRAME_MS = 16         # ~60fps
HOVER_ANIM_DECAY = 0.25    # 颜色指数衰减系数（越大越快）
PRESS_SCALE_MS = 100       # 按下缩放持续时间
PULSE_DURATION_MS = 300    # 模式切换脉冲总时长
PULSE_WIDTH_DELTA = 6      # 脉冲时环宽增量

# 进度条动画
PROGRESS_DECAY = 0.15      # 指数衰减系数

# ============================================================
#  默认时长（分钟）
# ============================================================
DEFAULT_WORK_MIN = 30
DEFAULT_SHORT_BREAK_MIN = 6
DEFAULT_LONG_BREAK_MIN = 20

# 长休息触发间隔（每 N 次专注后）
LONG_BREAK_INTERVAL = 4
