# face_engine.py
import time
import face_display

# Mood face mappings
MOOD_FACES = {
    "happy": "kids_happy",
    "sad": "sleeping",       # Placeholder; add sad.png if you want
    "angry": "thinking",     # Placeholder; add angry.png if you want
    "neutral": "normal"
}

# Command face mappings
COMMAND_FACES = {
    "time": "normal",
    "date": "normal",
    "joke": "kids_happy",
    "mood": "normal",  # Mood commands show mood face separately
    "quran": "quran_mode",
    "prayer": "normal",
    "story": "kids_happy",
    "music": "kids_happy",
    "tariq_shutdown": "sleeping",
    "tariq_restart": "thinking",
    "system_shutdown": "sleeping",
    "system_restart": "thinking",
    "error": "error",
    "unknown": "error"
}

def show_face_for_mood(mood, duration=3):
    face_name = MOOD_FACES.get(mood, "normal")
    face_display.display_face(face_name, duration)

def show_face_for_command(command_key, duration=3):
    face_name = COMMAND_FACES.get(command_key, "normal")
    face_display.display_face(face_name, duration)
