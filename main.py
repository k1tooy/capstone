from gpiozero import LED
from time import sleep
import random

# Mapping class labels to GPIO pins, excluding "empty"
signal_pins = {"abnoy": 17, "fertilized": 27, "unfertilized": 22}

# Prepare LED objects
signals = {label: LED(pin) for label, pin in signal_pins.items()}


def sendSignal(label: str):
    led = signals.get(label)
    if led:
        led.on()
        sleep(0.5)
        led.off()


def getImage():
    pass


def identifyEgg():
    return random.choice(["abnoy", "empty", "fertilized", "unfertilized"])


def main():
    class_names = ["abnoy", "empty", "fertilized", "unfertilized"]

    while True:
        label = identifyEgg()
        print(f"Identified: {label}")
        if label != "empty":
            sendSignal(label)
        sleep(1)


if __name__ == "__main__":
    main()
