# quran_player.py

import os
import tts_manager

QURAN_AUDIO_PATH = "/home/pi/tariq_v1/assets/quran"

def play_quran(command_text=None, lang="ar"):
    try:
        # List all .mp3/.wav files
        files = sorted([f for f in os.listdir(QURAN_AUDIO_PATH) if f.lower().endswith(('.mp3', '.wav'))])
        if not files:
            msg = {
                "ar": "عذرًا، لا يوجد ملفات للقرآن.",
                "en": "Sorry, no Quran files available."
            }
            tts_manager.speak(msg[lang], lang)
            return

        # Select first file (can enhance later to parse surah from command_text)
        selected_file = files[0]
        file_path = os.path.join(QURAN_AUDIO_PATH, selected_file)

        print(f"[QuranPlayer] 🎵 Playing: {selected_file}")
        os.system(f"mpg123 '{file_path}' > /dev/null 2>&1")

        # Optionally say completion
        msg = {
            "ar": "تم تشغيل مقطع من القرآن.",
            "en": "Quran recitation played."
        }
        tts_manager.speak(msg[lang], lang)

    except Exception as e:
        print(f"[QuranPlayer] ❌ Playback error: {e}")
        fallback = {
            "ar": "حدث خطأ أثناء تشغيل القرآن.",
            "en": "Failed to play Quran audio."
        }
        tts_manager.speak(fallback[lang], lang)
