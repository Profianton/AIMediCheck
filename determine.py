import numpy as np
from glob import glob
from PIL import Image
from image_similarity_measures.quality_metrics import rmse   # root-mean-square error Berechnung
import threading


determine_dat={}
def reload():
    """Bilder neu laden
    """
    imgs=glob("classify_data/*/*.png")            # Bekannte Bilder werden eingelesen
    local_determine_dat={}
    for img_path in imgs:
        pill_type=img_path.split("\\")[1]
        local_determine_dat[pill_type]=local_determine_dat.get(pill_type,[])+[Image.open(img_path)]
    global determine_dat
    determine_dat=local_determine_dat

threading.Thread(target=reload).start()            # Bilder werden im Hintergrund geladen

def determine(img,options:list|None=None):
    """Tablettenbestimmung

    Args:
        img (Image.Image): Ausgerichtetes 1000x1000 Pixel Bild mit schwarzem Hintergrund
        options (list[str] | None, optional): Zu verwendete Tabletten.

    Returns:
        _type_: Name der Tablette
    """
    if options == None:
        options=determine_dat.keys()
    best_type,best_score=compare(img,rmse,options,0.006)  
    print(best_score,best_type)
    return best_type

def compare(img,func,options:list,max_score):
    """Finden des besten Tablettentyps basierend auf den eingegebenen Tablettentypoptionen, der eingegebenen Vergleichsfunktion und dem Maximalwert 

    Args:
        img (Image.Image): zu vergleichendes Bild
        func (callable): Vergleichsfunktion z.B. rmse
        options (list): erlaubte Tablettentypen
        max_score (float): Maximalwert, ab dem die Tablette als "unknown" klassifiziert wird.

    Raises:
        NotADirectoryError: Eine der Tablettenoptionen existiert nicht

    Returns:
        tuple[string, float]: Name und Ähnlichkeit der Tablette
    """
    while determine_dat=={}:
        pass
    best_type="unknown"
    best_score=max_score   # ab dem Maximalwert wird die Tablette als "unknown" klassifiziert
    for test_type in options:
        if test_type not in determine_dat.keys():
            raise NotADirectoryError(f"{test_type} does not exist at \"classify_data/\".")

        for test_img in determine_dat[test_type]:
            res=func(org_img=np.array(img), pred_img=np.array(test_img))
            if res<best_score:
                best_type=test_type
                best_score=res
    return best_type,best_score