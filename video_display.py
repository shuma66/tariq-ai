# video_display.py

import os

def play_video(name):
    path = f"/home/pi/tariq_v1/assets/video/{name}.mp4"
    if os.path.exists(path):
        print(f"[Video] Playing: {path}")
        os.system(f"mplayer -vo fbdev -zoom -x 480 -y 320 '{path}' > /dev/null 2>&1")
        # Clear framebuffer after playback
        os.system("sudo fbi -T 1 -d /dev/fb0 --noverbose --blank > /dev/null 2>&1")
    else:
        print(f"[Video] ❌ Not found: {path}")
