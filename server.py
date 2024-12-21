from fastapi import FastAPI, UploadFile
from fastapi import FastAPI
from PIL import Image
import io
from analyse import analyse
app = FastAPI()


from starlette.responses import FileResponse 

@app.get("/")
async def read_index():
    return FileResponse('index.html')


@app.post("/analyse")
async def create_upload_file(image: UploadFile):
    img=Image.open(io.BytesIO(await image.read()))
    pills_in_sample=analyse(img)
    out_img=Image.new("RGB",(img.width,int(img.height/8)))
    out_img.paste(img.resize((int(img.width/8),int(img.height/8))),(0,0))
    for i in range(sum(pills_in_sample.values())):
        out_img.paste(Image.open(f"{i}.png").resize((int(img.height/8),int(img.height/8))),(int(img.width/8)+int(img.height/8)*i,0))
    out_img.save("img.png")
    
    return {"pills": pills_in_sample}