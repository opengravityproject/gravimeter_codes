import time
import os
import subprocess
from datetime import datetime
from picamera2 import Picamera2

# ===== CONFIG =====
PIN = 4
INTERVAL_SECONDS = 60
CAPTURE_DIR = "data_images"
# ==================

os.makedirs(CAPTURE_DIR, exist_ok=True)

def laser_on():
    subprocess.run(["pinctrl", "set", str(PIN), "op", "dh"], check=True)

def laser_off():
    subprocess.run(["pinctrl", "set", str(PIN), "op", "dl"], check=True)

# --- Camera setup ---
picam2 = Picamera2()

# Still configuration but kept running continuously
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

# Small warm-up (important)
time.sleep(1)

try:
    while True:
        start = time.time()

        laser_on()
        time.sleep(5)
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = os.path.join(CAPTURE_DIR, f"capture_{timestamp}.jpg")
            picam2.capture_file(filename)
        finally:
            laser_off()

        elapsed = time.time() - start
        sleep_for = INTERVAL_SECONDS - elapsed
        if sleep_for > 0:
            time.sleep(sleep_for)

except KeyboardInterrupt:
    laser_off()
    picam2.stop()
    print("Stopped. Laser off, camera stopped.")

