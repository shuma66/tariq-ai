# story_teller.py

import random
import os
import tts_manager
import face_display

STORIES_DIR = "/home/pi/tariq_v1/assets/stories"

def get_random_story(lang):
    file_path = os.path.join(STORIES_DIR, f"stories_{lang.lower()}.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            stories = [line.strip() for line in f if line.strip()]
        if not stories:
            print("[StoryTeller] ❌ No stories found in file.")
            return None
        return random.choice(stories)
    except Exception as e:
        print(f"[StoryTeller] ❗️ Failed to load stories: {e}")
        return None

def tell_story(lang="ar"):
    story = get_random_story(lang)

    if not story:
        fallback = {
            "ar": "عذرًا، لا توجد قصص حالياً.",
            "en": "Sorry, I can't tell a story right now."
        }
        tts_manager.speak(fallback.get(lang, "No story available."), lang)
        return

    print(f"[StoryTeller] 📖 Telling story: {story}")
    face_display.display_face("story", duration=3)
    tts_manager.speak(story, lang)
