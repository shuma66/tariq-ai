# tts_manager.py

import os
import shutil
import threading

# === TTS ENGINE CHECK ===
def is_espeak_installed():
    return shutil.which("espeak-ng") is not None

# === SIMPLE SYNCHRONOUS SPEAK ===
def speak(text, lang="ar"):
    if not is_espeak_installed():
        print("[TTS] ❌ espeak-ng not found!")
        return

    if not text.strip():
        print("[TTS] ⚠️ Empty text; skipping speech.")
        return

    voice = "ar" if "ar" in lang else "en"
    print(f"[TTS] 🔊 Speaking in {voice}: {text}")
    os.system(f'espeak-ng -v {voice} "{text}" 2>/dev/null')

# === OPTIONAL PARALLEL SPEAK ===
def threaded_speak(text, lang="ar"):
    thread = threading.Thread(target=speak, args=(text, lang), daemon=True)
    thread.start()
    return thread
