## audio output
import simpleaudio as sa
import os

def play_audio(filename):
    path = os.path.join(os.path.dirname(__file__), "..", "sounds", filename)
    try:
        wave_obj = sa.WaveObject.from_wave_file(path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"[AudioOutput] Failed to play {filename}: {e}")
