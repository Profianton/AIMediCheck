import numpy as np
from glob import glob
from PIL import Image
from image_similarity_measures.quality_metrics import rmse



imgs=glob("classify_data/*/*.png")
determine_dat={}
for img_path in imgs:
    pill_type=img_path.split("\\")[1]
    determine_dat[pill_type]=determine_dat.get(pill_type,[])+[Image.open(img_path)]

def determine(img,options:list|None=None):
    if options == None:
        options=determine_dat.keys()
    best_type="unknown"
    best_score=.006
    for test_type in options:
        if test_type not in determine_dat.keys():
            raise NotADirectoryError(f"{test_type} does not exist at \"classify_data/\".")

        for test_img in determine_dat[test_type]:
            res=rmse(org_img=np.array(img), pred_img=np.array(test_img))
            if res<best_score:
                best_type=test_type
                best_score=res
    print(best_score,best_type)
    return best_type