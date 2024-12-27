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




# Load a model
model = YOLO(r'segment_YOLO\trained.pt')  # load a pretrained model

# img = Image.open(
#     r'yolov8\test\images\23_png.rf.f870d8d75eedb53cf4da43018381364d.jpg')

mask_mask=np.logical_not(np.array(Image.open("mask.png").convert("L")).astype(bool))

def segment_and_separate(img: Image.Image):
    """

    Args:
        img (Image.Image): Image to be Segmented

    Returns:
        list[tuple[Image.Image,Image.Image]]: list of pills and their masks (list[tuple[Pill,Mask]])
    """
    
    results = model(img,conf=0.93)  # predict on an image
    results[0].save('image.png')
    imgs = []
    for mask in results[0].masks.data:
        mask = np.array(mask)
        
        img_np = np.array(img)
        labeled_mask,num_features=ndimage.label(mask != 0)
        best_value=0

        for i in range(1,num_features+1):
            value=np.sum((labeled_mask==i))
            if value > best_value:
                best_value=value
                best_i=i
        mask=labeled_mask==best_i
        mask=scale_array(mask,img.size[::-1])
        img_np[np.logical_not(mask)] = [0, 0, 0]
        x_min, y_min, x_max, y_max = bounding_box(mask)
        out_img = Image.fromarray(img_np).crop((x_min, y_min, x_max, y_max))
        mask_img = Image.fromarray(mask).crop((x_min, y_min, x_max, y_max))
        imgs.append((out_img, mask_img))
    return imgs


def scale_array(arr, new_size):
    """
    Resizes a NumPy array like an image.
    Parameters:
        x (ndarray): The original NumPy array to be resized.
        new_size (tuple): The desired shape of the new array.
    Returns:
        ndarray: The resized NumPy array.
    """

    # factors = [old/new  for new, old in zip(new_size, arr.shape)]
    # def pixel(x, y):
    #     return arr[int(x*factors[0]), int(y*factors[1])]
    # g = np.vectorize(pixel)
    # return np.fromfunction(g, new_size)
    factors = [new/old for new, old in zip(new_size, arr.shape)]
    return ndimage.zoom(arr.astype(float), factors,order=1)>0.5