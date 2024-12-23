from PIL import Image
from cam import capture
from glob import glob
import light
from button import on_button_press
from client import analyse
@on_button_press
def capture_and_save()->Image.Image:
    print("capturing")
    global image
    path=f"images/{len(glob('images/*'))}.png"
    image=capture()
    image.save(path, compress_level=1)
    return image
while True:
    match input("cmd: "):
        case "pwm":
            light.high = float(input("Value (0-100): "))
            light.on()
        case "analyse":
            print(analyse(image))
        case _:
            capture_and_save()