import numpy as np
from scipy import ndimage
from PIL import Image
from bounding_box import bounding_box

def orient_pills(pills)->list[Image.Image]:
    pills_orientated=[]
    for pill,mask in pills:
        mask=np.array(mask).astype(bool)

        def grade_rotation_angle(angle):
            rotated_mask = ndimage.rotate(mask, angle, reshape=True)

            x_min, y_min, x_max, y_max=bounding_box(rotated_mask)
            return y_max-y_min

        angle = min(range(0,180,45),key=grade_rotation_angle)
        angle = min(range(angle-30,angle+40,10),key=grade_rotation_angle)
        angle = min(range(angle-5,angle+6,1),key=grade_rotation_angle)

        rotated_mask = ndimage.rotate(mask, angle, reshape=True)
        rotated_pill=pill.rotate(angle, expand=True).crop(bounding_box(rotated_mask))
        x_min, y_min, x_max, y_max=bounding_box(rotated_mask)
        new=Image.new("RGB",(1000,1000))
        new.paste(rotated_pill,(int(500-(x_max-x_min)/2),int(500-(y_max-y_min)/2)))
        pills_orientated.append(new)
    return pills_orientated
