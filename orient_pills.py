import numpy as np
from scipy import ndimage   
from PIL import Image
from bounding_box import bounding_box

def orient_pill(pill,mask):
    """richtet eine einzelne Tablette aus

    Args:
        pill (Image.Image): Tablettenbild
        mask (Image.Image): Mask

    Returns:
        Image.Image: Ausgerichtete Tablette
    """
    mask=np.array(mask).astype(bool)  # (True: Vordergrund; False: Hintergrund)

    def grade_rotation_angle(angle):
        rotated_mask = ndimage.rotate(mask, angle, reshape=True)

        x_min, y_min, x_max, y_max=bounding_box(rotated_mask)
        return y_max-y_min

    # Schrittweise herausfinden, des richtigen Rotationswinkels vom Groben zum Feinen
    angle = min(range(0,180,45),key=grade_rotation_angle)
    angle = min(range(angle-30,angle+40,20),key=grade_rotation_angle)
    angle = min(range(angle-10,angle+20,10),key=grade_rotation_angle)
    angle = min(range(angle-5,angle+6,2),key=grade_rotation_angle)
    angle = min(range(angle-1,angle+2,1),key=grade_rotation_angle)

    #Durchführen der Rotation mit dem herausgefunden Winkel angle
    rotated_mask = ndimage.rotate(mask, angle, reshape=True) 
    rotated_pill=pill.rotate(angle, expand=True).crop(bounding_box(rotated_mask))
    
    #Zentrieren auf einem 1000x1000 Pixel Bild
    x_min, y_min, x_max, y_max=bounding_box(rotated_mask)
    new=Image.new("RGB",(1000,1000))
    new.paste(rotated_pill,(int(500-(x_max-x_min)/2),int(500-(y_max-y_min)/2)))
    return new

def orient_pills(pills)->list[Image.Image]:
    """Richte Tabletten aus

    Args:
        pills (list[tuple[Image.Image, Image.Image]]): Tabletten mit ihren binären Masken 

    Returns:
        list[Image.Image]: Ausgerichtete Tabletten
    """
    pills_orientated=[orient_pill(pill,mask) for pill,mask in pills]

    return pills_orientated
