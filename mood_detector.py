# mood_detector.py content
def detect_mood(text):
    moods = {
        "happy": ["سعيد", "فرحان", "مبسوط", "happy", "great"],
        "sad": ["حزين", "زعلان", "sad"],
        "angry": ["غاضب", "معصب", "angry"]
    }
    text = text.lower()
    try:
        for mood, keywords in moods.items():
            if any(word in text for word in keywords):
                return mood
    except Exception as e:
        print(f"[MoodDetector] Error detecting mood: {e}")
    return "neutral"
