# joke_engine.py

import random
import os
import tts_manager
import face_display

JOKES_DIR = "/home/pi/tariq_v1/assets/jokes"

def get_random_joke(lang):
    file_path = os.path.join(JOKES_DIR, f"jokes_{lang.lower()}.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            jokes = [j.strip() for j in f.readlines() if j.strip()]
        if not jokes:
            return "عذرًا، لا توجد نكات متاحة الآن." if lang.startswith("ar") else "Sorry, no jokes available."
        return random.choice(jokes)
    except Exception as e:
        print(f"[JokeEngine] Failed to load jokes: {e}")
        return "عذرًا، لا يمكنني الوصول إلى النكات الآن." if lang.startswith("ar") else "Sorry, I can't access jokes right now."

def tell_joke(lang="ar"):
    joke = get_random_joke(lang)

    if not joke:
        fallback = {
            "ar": "عذرًا، لا توجد نكتة الآن.",
            "en": "Sorry, I don't have a joke right now."
        }
        tts_manager.speak(fallback.get(lang, "No joke available."), lang)
        return

    print(f"[JokeEngine] 🤣 Telling joke: {joke}")
    face_display.display_face("joke", duration=3)
    tts_manager.speak(joke, lang)
