import time
from segment_YOLO import segment_and_separate
from orient_pills import orient_pills
from PIL import Image
from determine import determine
import numpy as np

def analyse(img:Image.Image,options:list|None=None,types:list|None=None):
    print(f"Start:{time.time()}")
    pills=segment_and_separate(img)
    print(f"Segment&Sep:{time.time()}")
    
    pills=orient_pills(pills)
    print(f"Orient:{time.time()}")
    
    pills=list(filter(lambda pill: np.sum(np.array(pill))>20,pills))
    
    for i,pill in enumerate(pills):
        pill.save(f"{i}.png")
    print(f"Save:{time.time()}")
    
    pills_dict={}
    for pill in pills:
        pill_type=determine(pill,options)
        if types!=None:
            types.append(pill_type)
        pills_dict[pill_type]=pills_dict.get(pill_type,0)+1
    print(f"Determine:{time.time()}")
    return pills_dict
