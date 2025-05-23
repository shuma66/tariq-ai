# music_player.py

import os
import random
import tts_manager

MUSIC_DIR = "/home/pi/tariq_v1/assets/music"

def play_music(lang="ar"):
    try:
        # List only .mp3 or .wav files
        files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(('.mp3', '.wav'))]
        if not files:
            msg = {
                "ar": "لا توجد ملفات موسيقى.",
                "en": "No music files found."
            }
            tts_manager.speak(msg.get(lang, msg["en"]), lang)
            return

        # Pick a random song
        song = random.choice(files)
        song_path = os.path.join(MUSIC_DIR, song)

        msg = {
            "ar": "سوف أبدأ تشغيل الموسيقى الآن.",
            "en": "Starting music playback now."
        }
        tts_manager.speak(msg.get(lang, msg["en"]), lang)

        print(f"[MusicPlayer] 🎵 Now playing: {song}")
        os.system(f"mpg123 '{song_path}' > /dev/null 2>&1")

    except Exception as e:
        print(f"[MusicPlayer] ❌ Error: {e}")
        fallback = {
            "ar": "حدث خطأ أثناء تشغيل الموسيقى.",
            "en": "An error occurred while playing music."
        }
        tts_manager.speak(fallback.get(lang, fallback["en"]), lang)
