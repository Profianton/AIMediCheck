from time import sleep
import RPi.GPIO as GPIO
light_gpio = 26


GPIO.setmode(GPIO.BCM)
GPIO.setup(light_gpio, GPIO.OUT)


def on():
    GPIO.output(light_gpio, True)


def off():
    GPIO.output(light_gpio, False)

on()

def light_needed(f):
    def wrapper(*args, **kwargs):
        on()
        sleep(.1)
        out = f(*args, **kwargs)
        off()
        return out
    return wrapper
