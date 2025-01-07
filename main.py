from PIL import Image
from cam import capture
from glob import glob
import light
from button import on_button_press
from client import analyse
import rgb_led
@on_button_press
def capture_and_analyse():
    rgb_led.set_led([rgb_led.Color.BLUE,rgb_led.Color.BLACK])
    image=capture()
    res=analyse(image)
    print(res)
    if res["match"]:
        rgb_led.set_led(rgb_led.Color.GREEN)
    else:
        rgb_led.set_led(rgb_led.Color.RED)

def capture_and_save()->Image.Image:
    print("capturing")
    rgb_led.set_led(rgb_led.Color.YELLOW)
    global image
    path=f"images/{len(glob('images/*'))}.png"
    image=capture()
    image.save(path, compress_level=1)
    rgb_led.set_led(rgb_led.Color.GREEN)
    return image

while True:
    match input("cmd: "):
        case "analyse":
            print(analyse(image))
        case "s":
            capture_and_save()
        case _:
            capture_and_analyse()