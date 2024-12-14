from segment import segment_and_separate
from orient_pills import orient_pills
from PIL import Image
from determine import determine
import numpy as np

def analyse(img:Image.Image,options:list|None=None):
    
    pills=segment_and_separate(img)
    pills=orient_pills(pills)
    
    pills=list(filter(lambda pill: np.sum(np.array(pill))>20,pills))
    
    for i,pill in enumerate(pills):
        pill.save(f"{i}.png")
    
    pills_dict={}
    for pill in pills:
        pill_type=determine(pill,options)
        pills_dict[pill_type]=pills_dict.get(pill_type,0)+1
    return pills_dict
