import random
from gpiozero import LED
import time
from time import sleep
import os
from picamera2 import Picamera2

# Mapping class labels to GPIO pins, excluding "empty"
signal_pins = {"abnoy": 17, "fertilized": 27, "unfertilized": 22}

# Prepare LED objects
signals = {label: LED(pin) for label, pin in signal_pins.items()}


picam2 = Picamera2()
picam2.start()


def sendSignal(label: str):
    led = signals.get(label)
    if led:
        led.on()
        sleep(0.5)
        led.off()


def captureImage(path="captured"):
    os.makedirs(path, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(path, f"image_{timestamp}.jpg")
    picam2.capture_file(file_path)
    print(f"Image captured to {file_path}")
    return file_path


def moveImagePath(subfolder: str, file_name: str, output_dir="data"):
    path = os.path.join(output_dir, subfolder)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, f"{subfolder}_{file_name}.jpg")
    picam2.capture_file(file_path)
    print(f"Image captured to {file_path}")


def deleteImage(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted image: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")


def identifyEgg(image):
    # ML goes here
    # It must return a str value
    return random.choice(["abnoy", "empty", "fertilized", "unfertilized"])


def isFinished():
    pass


def main():
    class_names = ["abnoy", "empty", "fertilized", "unfertilized"]

    while True:
        image_path = captureImage()
        label = identifyEgg(image_path)
        print(f"Identified: {label}")

        if label != "empty":
            sendSignal(label)
            moveImagePath(label, image_path)
        else:
            deleteImage(image_path)

        sleep(1)


if __name__ == "__main__":
    main()
