# language_switcher.py

import json
import os

SETTINGS_FILE = os.path.expanduser("~/tariq_v1/settings.json")
SUPPORTED_LANGS = {"ar", "en"}
DEFAULT_LANG = "ar"

def get_current_language():
    """Returns current language code (e.g., 'ar' or 'en')"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                lang = settings.get("language", DEFAULT_LANG)
                base_lang = lang[:2]
                if base_lang in SUPPORTED_LANGS:
                    return lang
                else:
                    print(f"[LangSwitcher] Unsupported lang in settings: {lang}")
        except Exception as e:
            print(f"[LangSwitcher] ⚠️ Failed to read settings: {e}")
    return DEFAULT_LANG

def set_language(lang_code):
    """Sets language and writes to settings.json"""
    base_lang = lang_code[:2]
    if base_lang not in SUPPORTED_LANGS:
        print(f"[LangSwitcher] ❌ Unsupported language: {lang_code}")
        return False

    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({"language": lang_code}, f)
        print(f"[LangSwitcher] ✅ Language set to: {lang_code}")
        return True
    except Exception as e:
        print(f"[LangSwitcher] ❗️ Failed to write settings: {e}")
        return False

def toggle_language():
    """Switch between AR and EN"""
    current = get_current_language()
    new_lang = "en" if current.startswith("ar") else "ar"
    if set_language(new_lang):
        return new_lang
    return current
