# command_matcher.py — Face display removed, video enabled

import os
import sys
import time

from tts_manager import speak
from mood_detector import detect_mood
from joke_engine import tell_joke
from prayer_times import say_time, say_date
from prayer_manager import say_prayer_times
from quran_player import play_quran
from story_teller import tell_story
from music_player import play_music
from hadith_reader import read_hadith
from command_logger import log_command
from video_engine import play_video
from language_switcher import toggle_language

def handle_command(command_text, lang="ar"):
    command_text = command_text.lower()
    print(f"[CommandMatcher] Received command: '{command_text}' in language: {lang}")

    start_time = time.time()

    try:
        # LANGUAGE SWITCH
        if any(word in command_text for word in ["language", "لغة", "english", "مصري"]):
            new_lang = toggle_language()
            speak({
                "ar": "تم تغيير اللغة إلى العربية.",
                "en": "Language switched to English."
            }[new_lang], new_lang)
            duration = time.time() - start_time
            log_command(command_text, "toggle_language", new_lang, duration)
            return "toggle_language"

        # TIME
        elif any(word in command_text for word in ["وقت", "الساعة", "time"]):
            play_video("Thinking.mp4")
            say_time(lang)
            duration = time.time() - start_time
            log_command(command_text, "time", lang, duration)
            return "time"

        # DATE
        elif any(word in command_text for word in ["تاريخ", "اليوم", "date"]):
            play_video("Thinking.mp4")
            say_date(lang)
            duration = time.time() - start_time
            log_command(command_text, "date", lang, duration)
            return "date"

        # JOKE
        elif any(word in command_text for word in ["نكتة", "joke"]):
            play_video("Happy.mp4")
            joke = tell_joke(lang)
            speak(joke, lang)
            duration = time.time() - start_time
            log_command(command_text, "joke", lang, duration)
            return "joke"

        # MOOD
        elif any(word in command_text for word in ["مزاج", "كيف", "تشعر", "mood", "how are you"]):
            mood = detect_mood(command_text)
            mood_video = {
                "happy": "Happy.mp4",
                "sad": "Sad.mp4",
                "angry": "Angry.mp4"
            }.get(mood, "Thinking.mp4")
            play_video(mood_video)
            response = {
                "ar": f"أشعر أن مزاجك {mood}",
                "en": f"I think you're feeling {mood}"
            }[lang]
            speak(response, lang)
            duration = time.time() - start_time
            log_command(command_text, "mood", lang, duration)
            return "mood"

        # QURAN
        elif any(word in command_text for word in ["قرآن", "quran"]):
            play_video("quran_mode.mp4")
            play_quran(command_text, lang)
            duration = time.time() - start_time
            log_command(command_text, "quran", lang, duration)
            return "quran"

        # PRAYER
        elif any(word in command_text for word in ["صلاة", "prayer"]):
            play_video("Thinking.mp4")
            say_prayer_times(lang)
            duration = time.time() - start_time
            log_command(command_text, "prayer", lang, duration)
            return "prayer"

        # STORY
        elif any(word in command_text for word in ["قصة", "story"]):
            play_video("Waiting.mp4")
            tell_story(lang)
            duration = time.time() - start_time
            log_command(command_text, "story", lang, duration)
            return "story"

        # MUSIC
        elif any(word in command_text for word in ["موسيقى", "اغاني", "مزيكا", "music", "song", "play"]):
            play_video("Happy.mp4")
            play_music(lang)
            duration = time.time() - start_time
            log_command(command_text, "music", lang, duration)
            return "music"

        # HADITH
        elif any(word in command_text for word in ["حديث", "hadith"]):
            play_video("Thinking.mp4")
            read_hadith(lang)
            duration = time.time() - start_time
            log_command(command_text, "hadith", lang, duration)
            return "hadith"

        # SHUTDOWN
        elif any(word in command_text for word in ["إيقاف", "اغلاق"]) and lang == "ar":
            speak("جاري إغلاق المساعد.", lang)
            play_video("Error.mp4")
            duration = time.time() - start_time
            log_command(command_text, "tariq_shutdown", lang, duration)
            time.sleep(2)
            exit(0)

        # RESTART
        elif any(word in command_text for word in ["إعادة تشغيل", "اعادة تشغيل"]) and lang == "ar":
            speak("جاري إعادة تشغيل المساعد.", lang)
            play_video("Error.mp4")
            duration = time.time() - start_time
            log_command(command_text, "tariq_restart", lang, duration)
            time.sleep(2)
            os.execv(sys.executable, ['python3'] + sys.argv)

        # SYSTEM SHUTDOWN (English only)
        elif lang == "en" and any(word in command_text for word in ["power off", "shutdown", "system shutdown"]):
            speak("Shutting down the system.", lang)
            play_video("Error.mp4")
            duration = time.time() - start_time
            log_command(command_text, "system_shutdown", lang, duration)
            time.sleep(2)
            os.system("sudo shutdown now")
            return "system_shutdown"

        # SYSTEM RESTART (English only)
        elif lang == "en" and any(word in command_text for word in ["restart", "reboot", "system restart"]):
            speak("Restarting the system.", lang)
            play_video("Error.mp4")
            duration = time.time() - start_time
            log_command(command_text, "system_restart", lang, duration)
            time.sleep(2)
            os.system("sudo reboot")
            return "system_restart"

        # FALLBACK
        else:
            speak({
                "ar": "لم أفهم الأمر.",
                "en": "I didn't understand that."
            }[lang], lang)
            play_video("Error.mp4")
            duration = time.time() - start_time
            log_command(command_text, "unknown", lang, status="unknown", duration=duration)
            return "unknown"

    except Exception as e:
        print(f"[CommandMatcher] ❌ Error: {e}")
        speak({
            "ar": "حدث خطأ أثناء تنفيذ الأمر.",
            "en": "An error occurred while processing the command."
        }[lang], lang)
        play_video("Error.mp4")
        duration = time.time() - start_time
        log_command(command_text, "error", lang, status="fail", duration=duration)
        return "error"
