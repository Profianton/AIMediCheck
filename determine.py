import time
import numpy as np
from glob import glob
from PIL import Image
from image_similarity_measures.quality_metrics import rmse   # root-mean-square error Berechnung
import threading
import math

determine_dat={}
determine_dat_low_res={}
def reload():
    """Bilder neu laden
    """
    imgs=glob("classify_data/*/*.png")            # Bekannte Bilder werden eingelesen
    local_determine_dat={}
    for img_path in imgs:
        pill_type=img_path.split("\\")[1]
        local_determine_dat[pill_type]=local_determine_dat.get(pill_type,[])+[Image.open(img_path)]
    local_determine_dat_low_res={
        pill_type:[
            img.resize((250,250))
            for img in imgs
            ] for pill_type,imgs in local_determine_dat.items()}
    local_determine_dat_low_res={
        pill_type:[
            np.array(img)
            for img in imgs
            ] for pill_type,imgs in local_determine_dat_low_res.items()}
    local_determine_dat={
        pill_type:[
            np.array(img)
            for img in imgs
            ] for pill_type,imgs in local_determine_dat.items()}
    
    global determine_dat,determine_dat_low_res
    determine_dat_low_res=local_determine_dat_low_res
    determine_dat=local_determine_dat


def determine(img,options:list|None=None):
    """Tablettenbestimmung

    Args:
        img (Image.Image): Ausgerichtetes 1000x1000 Pixel Bild mit schwarzem Hintergrund
        options (list[str] | None, optional): Zu verwendende Tabletten.

    Returns:
        str: Name der Tablette
    """
    while determine_dat=={}:
        pass
    if options == None:
        options=determine_dat.keys()
    scores={}
    best_type,best_score=compare(np.array(img),rmse,{option:determine_dat_low_res[option] for option in options},0.006,scores)  
    #best_type,best_score=compare(np.array(img.resize((250,250))),rmse,{option:determine_dat_low_res[option] for option in options},0.006,scores)  
    print(best_score,best_type)
    return best_type

def compare(img,func,options:dict[str:list],max_score,scores:dict={}):
    best_type="unknown"
    best_score=max_score   # ab dem Maximalwert wird die Tablette als "unknown" klassifiziert
    for test_type,test_imgs in options.items():
        best_current_type_score=math.inf
        for test_img in test_imgs:
            res=func(org_img=img, pred_img=test_img)
            if res<best_current_type_score:
                best_current_type_score=res
        if best_current_type_score<best_score:
                best_type=test_type
                best_score=best_current_type_score
        scores[test_type]=best_current_type_score
    return best_type,best_score

if __name__=="__main__":
    reload()
    imgs=["0.png","1.png","2.png"]
    imgs=[Image.open(img) for img in imgs]
    start=time.time()
    for img in imgs:
        determine(img)
    print(time.time()-start)
else:
    threading.Thread(target=reload).start()            # Bilder werden im Hintergrund geladen