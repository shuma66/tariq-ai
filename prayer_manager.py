import os
import time
from datetime import datetime
import sounddevice as sd
import tts_manager
from prayer_times_calculator import PrayerTimesCalculator

# === CONFIGURATION ===
LOCATION = {
    "latitude": 30.01541,
    "longitude": 31.41887,
    "timezone": 3  # Cairo timezone UTC+3
}

ADHAN_FOLDER = "/home/pi/Music/Adhan"

PRAYER_ADHANS = {
    "Fajr": "Adhan-fajr.mp3",
    "Dhuhr": "Adhan-Makkah.mp3",
    "Asr": "Adhan-Madinah.mp3",
    "Maghrib": "Adhan-Turkish.mp3",
    "Isha": "Adhan-Mishary-Rashid-Al-Afasy.mp3"
}

ARABIC_PRAYER_NAMES = {
    "Fajr": "الفجر",
    "Dhuhr": "الظهر",
    "Asr": "العصر",
    "Maghrib": "المغرب",
    "Isha": "العشاء"
}

# === UTILS ===
def release_audio_devices():
    try:
        sd.stop()
        print("[Audio] Released audio devices before Adhan playback.")
    except Exception as e:
        print(f"[Audio] Failed to release audio devices: {e}")

# === PRAYER TIMES CALCULATION ===
def get_today_prayers():
    try:
        pt = PrayerTimesCalculator(
            latitude=LOCATION["latitude"],
            longitude=LOCATION["longitude"],
            calculation_method="egypt",
            date=datetime.now().strftime("%Y-%m-%d")
        )
        times = pt.fetch_prayer_times()
        return times
    except Exception as e:
        print(f"[PrayerManager] Failed to calculate prayer times: {e}")
        return {}

# === ADHAN PLAYBACK ===
def play_adhan(prayer_name):
    filename = PRAYER_ADHANS.get(prayer_name)
    if not filename:
        print(f"[PrayerManager] No Adhan configured for {prayer_name}")
        return

    file_path = os.path.join(ADHAN_FOLDER, filename)
    if not os.path.isfile(file_path):
        print(f"[PrayerManager] Adhan file not found: {file_path}")
        return

    try:
        release_audio_devices()
        print(f"[PrayerManager] Playing Adhan for {prayer_name} with mpg123.")
        os.system(f"mpg123 '{file_path}' > /dev/null 2>&1")
        print("[PrayerManager] Adhan playback finished.")
    except Exception as e:
        print(f"[PrayerManager] Error during Adhan playback: {e}")

# === PRAYER CHECK ===
def check_and_play_prayer():
    prayers = get_today_prayers()
    if not prayers:
        print("[PrayerManager] No prayer times available.")
        return

    now = datetime.now().strftime('%H:%M')
    for name, time_str in prayers.items():
        if name not in PRAYER_ADHANS:
            continue
        if now == time_str[:-3]:
            print(f"[PrayerManager] It's time for {name} prayer ({time_str})")
            play_adhan(name)
            break

# === TIME ===
def say_time(lang="ar"):
    now = datetime.now().strftime("%I:%M %p")
    msg = {
        "ar": f"الساعة الآن {now}",
        "en": f"The time is {now}"
    }.get(lang[:2], f"The time is {now}")
    print(f"[PrayerManager] {msg}")
    tts_manager.speak(msg, lang)

def say_date(lang="ar"):
    today = datetime.now().strftime("%Y-%m-%d")
    msg = {
        "ar": f"اليوم هو {today}",
        "en": f"Today is {today}"
    }.get(lang[:2], f"Today is {today}")
    print(f"[PrayerManager] {msg}")
    tts_manager.speak(msg, lang)

# === NEXT PRAYER ===
def say_next_prayer(lang="ar"):
    prayers = get_today_prayers()
    if not prayers:
        fallback = {
            "ar": "لا أستطيع حساب مواعيد الصلاة الآن.",
            "en": "I cannot calculate prayer times right now."
        }
        tts_manager.speak(fallback.get(lang[:2], fallback["en"]), lang)
        return

    now = datetime.now().strftime('%H:%M')
    upcoming = None

    for name in PRAYER_ADHANS:
        time_str = prayers.get(name)
        if not time_str:
            continue
        if now < time_str[:-3]:
            upcoming = (name, time_str)
            break

    if upcoming:
        name, time_str = upcoming
        msg = {
            "ar": f"الصلاة القادمة هي {ARABIC_PRAYER_NAMES.get(name, name)} في تمام الساعة {time_str}",
            "en": f"The next prayer is {name} at {time_str}"
        }.get(lang[:2], f"The next prayer is {name} at {time_str}")
    else:
        msg = {
            "ar": "لا توجد صلوات أخرى اليوم.",
            "en": "No more prayers for today."
        }.get(lang[:2], "No more prayers for today.")

    print(f"[PrayerManager] {msg}")
    tts_manager.speak(msg, lang)

# === COMBINED PRAYER INFO ===
def tell_prayer_info(lang="ar"):
    say_time(lang)
    say_next_prayer(lang)

# === FULL PRAYER TIME SUMMARY ===
def say_prayer_times(lang="ar"):
    prayers = get_today_prayers()
    if not prayers:
        fallback = {
            "ar": "عذرًا، لا يمكنني الحصول على مواقيت الصلاة الآن.",
            "en": "Sorry, I couldn't retrieve the prayer times."
        }
        tts_manager.speak(fallback.get(lang[:2], fallback["en"]), lang)
        return

    lines = []
    if lang.startswith("ar"):
        lines.append("مواقيت الصلاة لليوم:")
        for name in PRAYER_ADHANS:
            time_str = prayers.get(name)
            if time_str:
                lines.append(f"{ARABIC_PRAYER_NAMES.get(name, name)} في {time_str}")
    else:
        lines.append("Today's prayer times are:")
        for name in PRAYER_ADHANS:
            time_str = prayers.get(name)
            if time_str:
                lines.append(f"{name} at {time_str}")

    full_message = ". ".join(lines)
    print(f"[PrayerManager] {full_message}")
    tts_manager.speak(full_message, lang)

# === ENTRY POINT ===
if __name__ == "__main__":
    check_and_play_prayer()
