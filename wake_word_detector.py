# wake_word_detector.py
import time
import os
import signal
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

DEFAULT_MODEL_PATH = "/home/pi/vosk-model-small-ar-0.22"
wake_words = ["طارئ","طارق", "tariq"]

q = queue.Queue(maxsize=20)
running = True

def callback(indata, frames, time, status):
    if status:
        print("[WakeWord] Status:", status)
    q.put(bytes(indata))  # Ensures data is in raw bytes (not numpy buffer)

def signal_handler(sig, frame):
    global running
    print("\n[WakeWord] 🔕 Signal received. Stopping listener...")
    running = False

def listen_for_wake_word(device=None, model_path=DEFAULT_MODEL_PATH):
    global running
    running = True  # reset before each call

    if not os.path.exists(model_path):
        print(f"[WakeWord] ❗️ Vosk model not found at: {model_path}")
        return False

    try:
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 44100)
    except Exception as e:
        print(f"[WakeWord] ❌ Failed to load model: {e}")
        return False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        with sd.RawInputStream(samplerate=44100, blocksize=2048, device=device,
                               dtype='int16', channels=1, callback=callback):
            print("[WakeWord] 🎧 Listening for wake word...")

            while running:
                if not q.empty():
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").lower()
                        print(f"[WakeWord] Heard: {text}")
                        if any(word in text for word in wake_words):
                            print("[WakeWord] ✅ Wake word detected.")
                            return True
                    time.sleep(0.01)  # ✅ Helps reduce CPU overload and buffer overflow

    except Exception as e:
        print(f"[WakeWord] ⚠️ Audio input error: {e}")
        return False

    print("[WakeWord] 🔕 Listener exited.")
    return False
