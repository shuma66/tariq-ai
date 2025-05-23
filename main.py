# Tariq Main Script – Cleaned version (face display optional)

import os
import signal
import sys
import json
import queue
import time
import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
from wake_word_detector import listen_for_wake_word
from audio_input import record_audio, cleanup_audio, release_audio_devices
from command_matcher import handle_command
import language_switcher
import tts_manager
from performance_logger import Timer

# Optional: enable or disable face display
USE_FACES = False
if USE_FACES:
    from face_display import display_face

WAKE_CONFIRMATION_SOUND = "assets/sounds/wake_confirmation.wav"
running = True
model = None
rec = None

def play_wake_confirmation():
    try:
        print("[System] 🎵 Playing wake confirmation sound.")
        os.system(f'aplay {WAKE_CONFIRMATION_SOUND} > /dev/null 2>&1')
    except Exception as e:
        print(f"[Error] Failed to play wake confirmation sound: {e}")

def signal_handler(sig, frame):
    global running
    print("\n[System] ⚠️ Interrupt received. Cleaning up...")
    running = False

    try:
        release_audio_devices()
    except Exception as e:
        print(f"[Cleanup] Audio release failed: {e}")

    print("[System] ✅ Tariq shut down cleanly.")
    sys.exit(0)

def transcribe_audio(path, rec):
    with sf.SoundFile(path) as audio_file:
        while True:
            data = audio_file.read(4000, dtype='int16')
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data.tobytes()):
                break
    result = json.loads(rec.FinalResult())
    return result.get("text", "").strip()

def main():
    global running, model, rec
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("[Tariq AI] 🚀 Starting assistant...")
    current_lang = language_switcher.get_current_language()
    print(f"[Language] 🌐 Language: {current_lang}")

    model_path = {
        "ar": "/home/pi/vosk-model-small-ar-0.22",
        "en": "/home/pi/vosk-model-small-en-us-0.15"
    }.get(current_lang[:2], "/home/pi/vosk-model-small-ar-0.22")

    if not os.path.exists(model_path):
        print(f"[Error] ❗️ Vosk model not found: {model_path}")
        sys.exit(1)

    print(f"[Vosk] Loading model from: {model_path}")
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    while running:
        print("[Main] 🐾 Waiting for wake word...")
        try:
            if listen_for_wake_word():
                play_wake_confirmation()

                if USE_FACES:
                    try:
                        display_face("thinking")
                    except Exception as e:
                        print(f"[FaceDisplay] ⚠️ Failed to show face: {e}")

                with Timer("Audio Recording"):
                    audio_path = record_audio()

                if audio_path:
                    try:
                        with Timer("STT"):
                            recognized_text = transcribe_audio(audio_path, rec)
                        print(f"[STT] 📝 Recognized text: {recognized_text}")

                        with Timer("Command Execution"):
                            command = handle_command(recognized_text, current_lang)
                        print(f"[Command] ✅ Processed: {command}")

                        # 🔁 Reload language if changed
                        new_lang = language_switcher.get_current_language()
                        if new_lang != current_lang:
                            print(f"[Language] 🔄 Language changed to: {new_lang}")
                            current_lang = new_lang
                            # Optionally reload model if needed
                            new_model_path = {
                                "ar": "/home/pi/vosk-model-small-ar-0.22",
                                "en": "/home/pi/vosk-model-small-en-us-0.15"
                            }.get(current_lang[:2], "/home/pi/vosk-model-small-ar-0.22")
                            if new_model_path != model_path:
                                model_path = new_model_path
                                print(f"[Vosk] 🔁 Reloading model: {model_path}")
                                model = Model(model_path)
                                rec = KaldiRecognizer(model, 16000)

                    except Exception as e:
                        print("[Error] ❗️Command error:", e)
                        fallback = {
                            "ar": "حدث خطأ أثناء معالجة الأمر.",
                            "en": "There was an error processing your command."
                        }
                        tts_manager.speak(fallback.get(current_lang, "Unknown error."), current_lang)
                    finally:
                        cleanup_audio(audio_path)
                else:
                    print("[AudioInput] ⚠️ No audio recorded.")
        except Exception as e:
            print(f"[Error] Wake word loop exception: {e}")

    signal_handler(None, None)

if __name__ == "__main__":
    main()
