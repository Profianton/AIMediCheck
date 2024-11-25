from rembg import remove
from PIL import Image
from glob import glob
for image in glob("images/*"):
    input_img=Image.open(image)
    img = remove(input_img)
    for x in range(img.size[0]):    # for every pixel:
        for y in range(img.size[1]):
            if img.getpixel((x,y))!=(0,0,0,0):
                img.putpixel((x,y),(255,255,255,255))
    print(image)
    img.save(image.replace("images","annotations"))