
import RPi.GPIO as GPIO
light_gpios = [13,26]


GPIO.setmode(GPIO.BCM)
GPIO.setup(light_gpios, GPIO.OUT)

def on():
    GPIO.output(light_gpios, True)
        

def off():
    GPIO.output(light_gpios, False)


on()