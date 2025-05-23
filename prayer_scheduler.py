import time
import prayer_manager

def run_scheduler():
    while True:
        prayer_manager.check_and_play_prayer()
        time.sleep(60)  # wait 60 seconds

if __name__ == "__main__":
    run_scheduler()
