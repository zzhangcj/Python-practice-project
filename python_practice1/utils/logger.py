import datetime
import os

from config import LOG_FILE


# ===== 统一日志写入 =====
def write_log(content):
    """写入日志到文件，返回日志行内容"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{current_time}] {content}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

    return log_line
