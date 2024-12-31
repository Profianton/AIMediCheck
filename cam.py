import os                   # Umgebungsvariablen setzen
from PIL import Image       # Bildbearbeitung
from picamera2 import Picamera2  # Kameraansteuerung
from libcamera import controls  # Kameraansteuerung

# Unterdrückt Textausgabe der Kamera
os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

# Initialisierung der Kamera
picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual,
                    "LensPosition": 11.44})  # Fokus setzen


def capture():
    """Bild aufnehmen und zuschneiden

    Returns:
        Image.Image: Aufgenommenes und zugeschnittenes Bild
    """
    image: Image.Image = picam2.switch_mode_and_capture_image(capture_config)
    image = image.crop((1000, 120, 3600, 2592))
    return image
