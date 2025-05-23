# hadith_reader.py content
import random
import os
import tts_manager

HADITH_DIR = "/home/pi/tariq_v1/assets/hadiths"

def get_random_hadith(lang):
    file_path = os.path.join(HADITH_DIR, f"hadiths_{lang.lower()}.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            hadiths = f.readlines()
        if not hadiths:
            return "Sorry, no hadiths available."
        return random.choice(hadiths).strip()
    except Exception as e:
        print(f"[HadithReader] Failed to load hadiths: {e}")
        return "Sorry, I can't access hadiths right now."

def read_hadith(lang):
    hadith = get_random_hadith(lang)
    tts_manager.speak(hadith, lang)
