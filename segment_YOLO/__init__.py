from PIL import Image
import os
os.environ["YOLO_VERBOSE"]="False"
from ultralytics import YOLO
import ultralytics
ultralytics.checks()
from PIL import Image
import numpy as np
from scipy import ndimage
from bounding_box import bounding_box




# Modell laden
model = YOLO(r'segment_YOLO\trained.pt')  

def segment_and_separate(img: Image.Image):
    """ Segmentieren und Separieren

    Args:
        img (Image.Image): Bild zum Segmentieren

    Returns:
        list[tuple[Image.Image,Image.Image]]: Liste von Tabletten und ihrer Masken (list[tuple[Pill,Mask]])
    """
    
    results = model(img,conf=0.93)  # Modell ausführen
    results[0].save('static/image.png')
    imgs = []
    if not results[0].masks:        # falls keine Tabletten vorhanden
        return []
    for mask in results[0].masks.data:
        mask = np.array(mask)
        
        img_np = np.array(img)
        
        # wenn das KI Modell ausgibt, dass eine Tablette aus 2 unverbundenen Stücken besteht, wähle das größere Stück
        labeled_mask,num_features=ndimage.label(mask != 0)
        best_value=0

        for i in range(1,num_features+1):  
            value=np.sum((labeled_mask==i))
            if value > best_value:
                best_value=value
                best_i=i
        mask=labeled_mask==best_i
        
        mask=scale_array(mask,img.size[::-1]) # Maske auf Bildgröße hochskalieren
        
        img_np[np.logical_not(mask)] = [0, 0, 0] # alles was außerhalb der Tablette ist, wird schwarz gefärbt
        # Tablette ausschneiden
        x_min, y_min, x_max, y_max = bounding_box(mask)
        out_img = Image.fromarray(img_np).crop((x_min, y_min, x_max, y_max))
        mask_img = Image.fromarray(mask).crop((x_min, y_min, x_max, y_max))
        
        imgs.append((out_img, mask_img))
    return imgs


def scale_array(arr, new_size):
    """NumPy Image hochskalieren

    Args:
        arr (ndarray): Ausgangsarray 
        new_size (tuple[int,int]): Wunschgröße des Zielarrays

    Returns:
        ndarray: Hochskalierter ndarray 
    """

    factors = [new/old for new, old in zip(new_size, arr.shape)]
    return ndimage.zoom(arr.astype(float), factors,order=1)>0.5