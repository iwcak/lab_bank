from datetime import datetime
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "logs.txt")


def log(action, details):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {action} | {details}\n")