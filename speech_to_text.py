##speech_to_text
from vosk import Model, KaldiRecognizer
import wave
import json
import os
import subprocess

vosk_models = {
    "ar": "/home/pi/vosk-model-small-ar-0.22",
    "en": "/home/pi/vosk-model-small-en-us-0.15"
}

models_cache = {}

def load_model(lang):
    lang_key = "ar" if lang.startswith("ar") else "en"
    print(f"[STT] Loading model for: {lang_key}")
    if lang_key not in models_cache:
        model_path = vosk_models.get(lang_key)
        if not model_path or not os.path.isdir(model_path):
            raise FileNotFoundError(f"Vosk model path not found: {model_path}")
        models_cache[lang_key] = Model(model_path)
    return models_cache[lang_key]

def convert_audio_to_16k_mono(input_path):
    converted_path = "/tmp/converted_input.wav"
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            "-sample_fmt", "s16",
            converted_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return converted_path
    except subprocess.CalledProcessError as e:
        print(f"[STT] ffmpeg conversion failed: {e}")
        return None

# audio_input.py
def playback_audio(file_path):
    try:
        print(f"[Playback] 🔊 Playing back: {file_path}")
        os.system(f"aplay {file_path}")
    except Exception as e:
        print(f"[Playback] ❌ Failed to play: {e}")


def transcribe_audio(audio_path, lang):
    if not audio_path or not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = load_model(lang)
    wf = wave.open(audio_path, "rb")

    if wf.getframerate() != 16000 or wf.getnchannels() != 1:
        print("[STT] Converting audio to 16kHz mono for Vosk compatibility...")
        wf.close()
        converted_path = convert_audio_to_16k_mono(audio_path)
        if not converted_path:
            raise RuntimeError("Audio conversion failed")
        wf = wave.open(converted_path, "rb")
    else:
        print("[STT] Audio format already valid.")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    try:
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                results.append(res.get("text", ""))
        res = json.loads(rec.FinalResult())
        results.append(res.get("text", ""))
    finally:
        wf.close()

    transcription = " ".join(results).strip()
    print(f"[STT] Transcription result: {transcription}")
    print(f"[STT Debug] Raw results: {results}")
    return transcription
