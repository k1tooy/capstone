from gpiozero import LED
import time
from time import sleep

import os
import shutil

from picamera2 import Picamera2
from picamera2 import Preview

from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf

# Mapping class labels to GPIO pins, excluding "empty" (yellow, orange, red)
signal_pins = {"balut": 17, "bugok": 27, "penoy": 22}

loaded_model = load_model(os.path.join("models", "balut_classifier4.h5"))

batch_size = 32
img_height = 180
img_width = 180

# Prepare LED objects
signals = {label: LED(pin) for label, pin in signal_pins.items()}


def has_display():
    # On headless systems, DISPLAY env variable is typically not set
    return (
        os.environ.get("DISPLAY") is not None
        or os.environ.get("WAYLAND_DISPLAY") is not None
    )


picam2 = Picamera2()

if has_display():
    try:
        picam2.start_preview(Preview.QT)
    except Exception as e:
        print(f"Preview failed to start: {e}")
else:
    print("No display detected. Skipping preview.")


picam2.start()


def sendSignal(label: str):
    led = signals.get(label)
    if led:
        led.on()
        print(f"Signal sent to {label} pin.")  # debugging purposes
        sleep(0.5)
        led.off()


def captureImage(path="captured"):
    os.makedirs(path, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(path, f"image_{timestamp}.jpg")
    picam2.capture_file(file_path)
    print(f"Image captured to {file_path}")
    return file_path


def moveImagePath(subfolder: str, source_path: str, output_dir="data"):
    file_name = os.path.basename(source_path)
    name_only, extension = os.path.splitext(file_name)

    target_dir = os.path.join(output_dir, subfolder)
    os.makedirs(target_dir, exist_ok=True)

    new_file_name = f"{subfolder}_{name_only}{extension}"
    destination_path = os.path.join(target_dir, new_file_name)

    shutil.move(source_path, destination_path)
    print(f"Image moved to {destination_path}")


def deleteImage(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted image: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")


def identifyEgg(image_path) -> str:
    class_names = ["balut", "bugok", "empty", "penoy"]

    img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Make prediction
    predictions = loaded_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    return class_names[np.argmax(score)]


def main():
    while True:
        sleep(5)
        image_path = captureImage()
        print(image_path)
        # image_path = "tests/balut_test_1.jpg"
        label = identifyEgg(image_path)
        print(f"Identified: {label}")

        if label != "empty":
            sleep(1)
            sendSignal(label)
            moveImagePath(label, image_path)
        else:
            deleteImage(image_path)


if __name__ == "__main__":
    main()
