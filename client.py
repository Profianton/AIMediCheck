import io
import requests
from PIL import Image

url = requests.get("https://drive.google.com/uc?export=download&id=1ODaG9aADGWhSKEZYQCMhcFxVehR57PyP").text


print(url)

def analyse(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    files = {'image': img_byte_arr}
    r = requests.post(f"{url}/analyse", files=files)
    return r.json()


if __name__=="__main__":
    img=Image.open(r'images\9.png')
    print(analyse(img))