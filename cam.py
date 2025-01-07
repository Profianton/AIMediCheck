import os                   # Umgebungsvariablen setzen
from PIL import Image       # Bildbearbeitung   
from picamera2 import Picamera2 #Kameraansteuerung
from libcamera import controls  #Kameraansteuerung

os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3" #Unterdrückt Textausgabe der Kamera

# Initialisierung der Kamera
picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.start()
#picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 11.44}) #Fokus setzen
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #Fokus setzen

def capture():
    """Bild aufnehmen und zuschneiden

    Returns:
        Image.Image: Aufgenommenes und zugeschnittenes Bild
    """
    image:Image.Image = picam2.switch_mode_and_capture_image(capture_config)
    image=image.crop((1125,280,3490,2580))
    return image