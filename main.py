from cam import capture
from glob import glob
import light

while True:
    match input("cmd: "):
        case "pwm":
            light.high = float(input("Value (0-100): "))
            light.on()
        case _:
            path=f"images/{len(glob('images/*'))}.png"
            capture().save(path, compress_level=1)
            