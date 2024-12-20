from time import sleep
import RPi.GPIO as GPIO
light_gpio = 26


GPIO.setmode(GPIO.BCM)
GPIO.setup(light_gpio, GPIO.OUT)

led = GPIO.PWM(light_gpio,100)

high=100
def on():
    # GPIO.output(light_gpio, True)
    led.start(high)

def off():
    # GPIO.output(light_gpio, False)
    led.start(0)


on()