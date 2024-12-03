from PIL import Image
import numpy as np
def combine(img,annotation):
    annotation=annotation.convert("L")
    annotation_array=np.array(annotation)
    img_array = np.array(img)
    img_array[annotation_array==0]=(0,0,0)
    out=Image.fromarray(img_array)
    return out