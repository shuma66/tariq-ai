# performance_logger.py

import time

class Timer:
    def __init__(self, label):
        self.label = label
        self.start = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        duration = time.time() - self.start
        print(f"[Timer] {self.label} took {duration:.2f} seconds.")
