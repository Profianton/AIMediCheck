
import RPi.GPIO as GPIO
light_gpio = 26


GPIO.setmode(GPIO.BCM)
GPIO.setup(light_gpio, GPIO.OUT)

def on():
    GPIO.output(light_gpio, True)


def off():
    GPIO.output(light_gpio, False)


on()