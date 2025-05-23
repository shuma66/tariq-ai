# prayer_times.py

import tts_manager
import prayer_manager

def say_time(lang="ar"):
    """Say the current time using tts_manager."""
    prayer_manager.say_time(lang)

def say_date(lang="ar"):
    """Say the current date using tts_manager."""
    prayer_manager.say_date(lang)

def say_next_prayer(lang="ar"):
    """Say the upcoming prayer time."""
    prayer_manager.say_next_prayer(lang)

def tell_prayer_info(lang="ar"):
    """Say time and next prayer info combined."""
    prayer_manager.tell_prayer_info(lang)
