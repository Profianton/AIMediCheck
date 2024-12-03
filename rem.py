import numpy as np
from PIL import Image,ImageFilter,ImageDraw
from glob import glob
mask_img=Image.open("mask.png")

for image in glob("images/*.png"):
    img=Image.open(image)

    img=Image.composite(img,Image.new("RGB",img.size),mask_img)

    img_array = np.array(img)
    sum_rg = img_array[:, :, 0]/2 + img_array[:, :, 1]/2
    mask = sum_rg > 15
    mask2 = sum_rg < 15
    img_array[mask] = [255, 255, 255]
    img_array[mask2] = [0, 0, 0]

    img = Image.fromarray(img_array).convert("L")
        
    img = img.filter(ImageFilter.GaussianBlur(radius=10))
    img_array = np.array(img)
    img_array[img_array != 255] = 0
    img = Image.fromarray(img_array)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=10))
    img_array = np.array(img)
    img_array[img_array != 0] = 255
    img = Image.fromarray(img_array)
    
    
    print(image)
    img.save(image.replace("images","annotations"))
