# video_engine.py — Non-blocking

import os
import subprocess
import threading

VIDEO_DIR = "/home/pi/tariq_v1/assets/video"
BLANK_CMD = "sudo fbi -T 1 -d /dev/fb0 --noverbose --blank > /dev/null 2>&1"

def _play(video_path):
    try:
        subprocess.run([
            "mplayer", "-vo", "fbdev", "-zoom", "-x", "480", "-y", "320", video_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[VideoEngine] ❗ Error during video playback: {e}")
    finally:
        os.system(BLANK_CMD)
        print("[VideoEngine] 🧹 Framebuffer cleared.")

def play_video(filename):
    video_path = os.path.join(VIDEO_DIR, filename)
    if not os.path.isfile(video_path):
        print(f"[VideoEngine] ❌ Video not found: {video_path}")
        return
    print(f"[VideoEngine] 🎬 Launching video: {filename}")
    threading.Thread(target=_play, args=(video_path,), daemon=True).start()
