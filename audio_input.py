#Audio Input 
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os

def record_audio(duration=4, samplerate=16000, channels=1):
    print("[AudioInput] 🎙️ Recording...")
    try:
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
        sd.wait()
    except Exception as e:
        print(f"[AudioInput] ❌ Recording failed: {e}")
        return None

    try:
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "user_input.wav")
        wav.write(temp_path, samplerate, audio)
        print(f"[AudioInput] ✅ Audio saved: {temp_path}")
        return temp_path
    except Exception as e:
        print(f"[AudioInput] ❌ Failed to save audio: {e}")
        return None

def cleanup_audio(file_path):
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"[AudioInput] 🧹 Removed: {file_path}")
    except Exception as e:
        print(f"[AudioInput] ⚠️ Cleanup failed: {file_path} — {e}")

def release_audio_devices():
    try:
        sd.stop()
        print("[AudioInput] 🔇 Audio devices released.")
    except Exception as e:
        print(f"[AudioInput] ⚠️ Failed to release audio: {e}")
