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


def captureImage(output_dir="captured", subfolder="default"):
    path = os.path.join(output_dir, subfolder)
    os.makedirs(path, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(path, f"image_{timestamp}.jpg")
    picam2.capture_file(file_path)
    print(f"Image captured to {file_path}")
    return file_path


def moveImagePath(subfolder: str, output_dir="data"):
    path = os.path.join(output_dir, subfolder)
    os.makedirs(path, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(path, f"image-{subfolder}_{timestamp}.jpg")
    picam2.capture_file(file_path)
    print(f"Image captured to {file_path}")
    return file_path


def deleteImage():
    pass


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
            moveImagePath(label)
        else:
            deleteImage()

        sleep(1)


if __name__ == "__main__":
    main()
