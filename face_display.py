# face_display.py – Optional face rendering (auto kill + optional GUI check)

import os
import time
import subprocess

def is_gui_active():
    return os.environ.get("DISPLAY") is not None

def display_face(face_name, duration=3):
    face_path = f"assets/faces/{face_name}.png"
    print(f"[FaceDisplay] Showing face: {face_path}")

    if not os.path.exists(face_path):
        print(f"[FaceDisplay] ⚠️ Face not found: {face_path}")
        return

    if is_gui_active():
        print("[FaceDisplay] GUI detected — using xdg-open.")
        subprocess.Popen(["xdg-open", face_path])
    else:
        print("[FaceDisplay] Headless — using fbi.")
        for fb in ["/dev/fb0", "/dev/fb1"]:
            try:
                subprocess.Popen(
                    ["sudo", "fbi", "-T", "1", "-d", fb, "-noverbose", "-a", face_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                time.sleep(duration)
                os.system("sudo killall fbi")
                break
            except Exception as e:
                print(f"[FaceDisplay] ⚠️ Display failed on {fb}: {e}")
