from cam import capture
from glob import glob
import light
from client import analyse

while True:
    match input("cmd: "):
        case "pwm":
            light.high = float(input("Value (0-100): "))
            light.on()
        case "analyse":
            print(analyse(image))
        case _:
            path=f"images/{len(glob('images/*'))}.png"
            image=capture()
            image.save(path, compress_level=1)
        
            