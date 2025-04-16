import os
import time
from picamera2 import Picamera2
from picamera2.previews.qt import Preview


def capture_image(output_dir="data", subfolder="default_subfolder"):
    # Create the full path for the subfolder within the output directory
    full_path = os.path.join(output_dir, subfolder)
    os.makedirs(full_path, exist_ok=True)

    picam2 = Picamera2()
    picam2.start_preview(Preview.QT)
    picam2.start()
    print("Press Enter to capture an image. Press Ctrl+C to exit.")

    count = 1

    while True:
        input()  # Wait for the user to press Enter
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(full_path, f"image_{timestamp}_{count}.jpg")
        picam2.capture_file(file_path)
        print(f"Image saved to {file_path}")
        count += 1


if __name__ == "__main__":
    capture_image()  # Default will use 'data' folder and 'default_subfolder'
