import io
import requests
from PIL import Image
import threading

url=""
def reload_url():
    global url
    url = requests.get("https://drive.google.com/uc?export=download&id=1ODaG9aADGWhSKEZYQCMhcFxVehR57PyP").text
    

threading.Thread(target=reload_url).start()

def analyse(img):
    while not url:
        pass
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    files = {'image': img_byte_arr}
    r = requests.post(f"{url}/analyse", files=files)
    try:
        return r.json()
    except:
        return {}


if __name__=="__main__":
    img=Image.open('/home/profianton/images/9.png')
    print(analyse(img))