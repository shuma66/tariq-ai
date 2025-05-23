import time
import threading
import tts_manager
import face_display

# Measure full round time
start = time.time()

def show_thinking_face():
    face_display.display_face("thinking", duration=3)

def speak_response():
    tts_manager.speak("أقوم الآن بتنفيذ الأمر. الرجاء الانتظار.", lang="ar")

# Start face display in a separate thread
face_thread = threading.Thread(target=show_thinking_face)
face_thread.start()

# Run TTS (blocking)
speak_response()

# Optional: wait for face to finish if needed
face_thread.join()

end = time.time()
print(f"[TEST] Total execution time: {end - start:.2f} seconds")
