# command_logger.py

import os
from datetime import datetime

LOG_DIR = "/home/pi/tariq_v1/logs"
LOG_FILE = os.path.join(LOG_DIR, "command_log.txt")
os.makedirs(LOG_DIR, exist_ok=True)

def log_command(text, command_key, lang, status="ok", duration=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dur_text = f"{duration:.2f}s" if duration is not None else "?"
    entry = f"[{timestamp}] ({lang}) [{status}] [{dur_text}] '{text}' → {command_key}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"[Logger] ❗️ Failed to log command: {e}")
