from time import sleep
import RPi.GPIO as GPIO

lights = {
    "r": 17,
    "g": 27,
    "b": 22
}


class Color:
    BLACK = 0
    RED = 1
    GREEN = 2    
    YELLOW = 3  
    BLUE = 4    
    PINK = 5    
    LIGHTBLUE = 5
    WHITE = 7


GPIO.setmode(GPIO.BCM)
GPIO.setup(lights.values(), GPIO.OUT)

# für rgb im Binärcode mit 3 Bits; 0: alle LEDs aus; 
masks = {
    "r": 2**0,  # rot: 2**0=1
    "g": 2**1,  # grün: 2**1=2
    "b": 2**2   # blau: 2**2=4; 
}


def set_led(val):
    """Setzt die rgb-LED auf eine bestimmte Farbe

    Args:
        val (int): rgb als Binärcode
    """
    val = int(val)
    for k, v in masks.items():
        GPIO.output(lights[k], bool(val & v))


if __name__ == "__main__":
    while 1:
        for i in range(8):
            set_led(i)
            sleep(1)
