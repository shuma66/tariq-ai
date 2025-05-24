# Tariq AI ✨ 🌙 طارق  
An Offline smart assistant for Raspberry Pi | Arabic &amp; English | Quran • Adhan • Stories • No Cloud Required

## 🧠 Overview

Tariq AI is an offline, culturally-aware voice assistant for Raspberry Pi devices. Designed to be educational, fun, and private — especially for kids and family-friendly environments — Tariq speaks Arabic and English, reacts with videos, recites Quran, plays Adhan, shares stories, jokes, and hadiths, and supports touch-screen interaction without requiring a phone or internet. Designed as a phone-free AI companion.

## 📦 Features

* ✅ Offline voice recognition (Vosk STT)
* ✅ Wake word detection ("Tariq")
* ✅ Multilingual support: Arabic 🇪🇬 & English 🇬🇧
* ✅ Quran mode with video animation
* ✅ Prayer time calculation & Adhan playback
* ✅ Jokes, stories, and hadiths support
* ✅ Mood detection & reaction videos
* ✅ Video-based UI (uses framebuffer)
* ✅ TTS engine (offline & clear)
* ✅ Fully local and secure

## 🖥️ Hardware Requirements

* Raspberry Pi 4/5
* 3.5" Touch LCD (or HDMI)
* Microphone & speaker (3.5mm or USB)
* Micro SD card (16GB+ recommended)

## ⚙️ Configuration – Set Your Location
Tariq AI uses your **geographic coordinates** to calculate accurate prayer times and Adhan schedules.

#To **set your location**, open the file:
prayer_times.py
# === CONFIGURATION ===
LOCATION = {
    "latitude": 30.091667,   # Example: Cairo
    "longitude": 31.630556,
    "timezone": 3            # UTC+3
}
##🔁 Change these values to match your city.
You can find your coordinates at latlong.net or via Google Maps.

#📍 Example: Jakarta, Indonesia
LOCATION = {
    "latitude": -6.2088,
    "longitude": 106.8456,
    "timezone": 7  # UTC+7
}
##⚠️ Note: Make sure to restart the assistant after updating your location.

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/tariq-ai.git
cd tariq-ai

# 2. Install requirements
python3 -m venv venv_tariq
source venv_tariq/bin/activate
pip install -r requirements.txt

# 3. Download Vosk models manually (Arabic + English)
# Place them in: /home/pi/vosk-model-small-ar-0.22 and /home/pi/vosk-model-small-en-us-0.15

# 4. Add execution permission to launcher script
chmod +x assets/launcher/run_tariq.sh
```

## 📂 Project Structure

```
tariq-ai/
├── main.py
├── command_matcher.py
├── tts_manager.py
├── wake_word_detector.py
├── quran_player.py
├── prayer_manager.py
├── language_switcher.py
├── video_engine.py
├── assets/
│   ├── launcher/run_tariq.sh
│   ├── video/*.mp4
│   ├── sounds/*.wav, *.mp3
│   ├── images/*.png
│   ├── faces/*.png
│   ├── jokes/jokes_ar.txt, jokes_en.txt
│   ├── stories/stories_ar.txt, stories_en.txt
│   ├── hadiths/hadiths_ar.txt, hadiths_en.txt

```

## 🧑‍💻 How to Use

Run Tariq via:

```bash
./assets/launcher/run_tariq.sh
```

Speak the wake word "طارق" or "Tariq" (depending on current language). Once awake, give voice commands like:

* "كم الساعة؟"
* "Tell me a joke"
* "ابدأ تشغيل القرآن"

Tariq will respond with audio and show matching video.

## 🌍 Language Toggle
## 📸 Screenshots

| Startup & Interface | Voice Commands | Kids & Language |
|---------------------|----------------|-----------------|
| ![Splash Start](assets/images/screenshots/splash_video_start.png) | ![Time Query](assets/images/screenshots/command_time.png) | ![Kids Mode](assets/images/screenshots/kids_interface.png) |
| ![Tariq Icon](assets/images/screenshots/tariq_desktop_icon.png) | ![Prayer Time](assets/images/screenshots/command_prayer_time.png) | ![Arabic → EN](assets/images/screenshots/language_toggle_en.png) |
| ![Wake Confirmed](assets/images/screenshots/wake_confirmation.png) | ![Quran Mode](assets/images/screenshots/command_quran_mode.png) | ![EN → Arabic](assets/images/screenshots/language_toggle_ar.png) |
| ![Error Fallback](assets/images/screenshots/error_fallback.png) | ![Joke in Arabic](assets/images/screenshots/command_joke_ar.png) | ![Hadith](assets/images/screenshots/command_hadith.png) |
| ![Requirements](assets/images/screenshots/requirements_list.png) | ![Story (AR)](assets/images/screenshots/command_story_ar.png) | ![Story (EN)](assets/images/screenshots/command_story_en.png) |

> All commands were spoken using the offline STT engine. Reactions are fully local with synchronized video.
Say:

"language" / "english" / "لغة" / "عربي"

Tariq will toggle between Arabic and English.

## ✨ Contributing

We welcome contributions, testing, and localization help!
Please fork the repo and create pull requests.

## ⚖️ License

MIT License — free to use and share with attribution.

---

Developed with guidance from ChatGPT and love from the creator.
Help us build meaningful smart assistants rooted in culture, language, and human values.
