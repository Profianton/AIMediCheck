import os
from PIL import Image
from picamera2 import Picamera2
from libcamera import controls
#from light import light_needed
os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 12})


#@light_needed
def capture():
    image:Image.Image = picam2.switch_mode_and_capture_image(capture_config)
    image=image.crop((1000,120,3600,2592))
    return image

for foc in range(20):
    print(foc)
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": foc})
    capture().save(f"focus/{foc}.png")
