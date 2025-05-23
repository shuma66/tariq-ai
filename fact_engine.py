# fact_engine.py content
import random
import os
import tts_manager

FACTS_DIR = "/home/pi/tariq_v1/assets/facts"

def get_random_fact(lang):
    file_path = os.path.join(FACTS_DIR, f"facts_{lang}.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            facts = f.readlines()
        if not facts:
            return "Sorry, no facts available."
        return random.choice(facts).strip()
    except Exception as e:
        print(f"[FactEngine] Failed to load facts: {e}")
        return "Sorry, I can't access facts right now."

def tell_fact(lang):
    fact = get_random_fact(lang)
    tts_manager.speak(fact, lang)
