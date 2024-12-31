import numpy as np
from scipy import ndimage   
from PIL import Image
from bounding_box import bounding_box

def orient_pills(pills)->list[Image.Image]:
    """Richte Tabletten aus

    Args:
        pills (list[tuple[Image.Image, Image.Image]]): Tabletten mit ihren binären Masken 

    Returns:
        list[Image.Image]: Ausgerichtete Tabletten
    """
    pills_orientated=[]
    for pill,mask in pills:
        mask=np.array(mask).astype(bool)  # (True: Vordergrund; False: Hintergrund)

        def grade_rotation_angle(angle):
            rotated_mask = ndimage.rotate(mask, angle, reshape=True)

            x_min, y_min, x_max, y_max=bounding_box(rotated_mask)
            return y_max-y_min

        # Schrittweise herausfinden, des richtigen Rotationswinkels vom Groben zum Feinen
        angle = min(range(0,180,45),key=grade_rotation_angle)
        angle = min(range(angle-30,angle+40,10),key=grade_rotation_angle)
        angle = min(range(angle-5,angle+6,1),key=grade_rotation_angle)

        #Durchführen der Rotation mit dem herausgefunden Winkel angle
        rotated_mask = ndimage.rotate(mask, angle, reshape=True) 
        rotated_pill=pill.rotate(angle, expand=True).crop(bounding_box(rotated_mask))
        
        #Zentrieren auf einem 1000x1000 Pixel Bild
        x_min, y_min, x_max, y_max=bounding_box(rotated_mask)
        new=Image.new("RGB",(1000,1000))
        new.paste(rotated_pill,(int(500-(x_max-x_min)/2),int(500-(y_max-y_min)/2)))
        pills_orientated.append(new)
    return pills_orientated
