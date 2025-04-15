import Rpi.GPIO as GPIO
import time


def sendSignal(pin: int):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()


def getImage():
    pass


def identifyEgg():
    import random

    return random.choice(["abnoy", "empty", "fertilized", "unfertilized"])


def main():
    class_names = ["abnoy", "empty", "fertilized", "unfertilized"]

    while True:
        label = identifyEgg()
        print(f"Identified: {label}")
        if label in signal_pins:
            sendSignal(signal_pins[label])
        time.sleep(1)


if __name__ == "__main__":
    main()
