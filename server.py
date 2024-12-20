from fastapi import FastAPI, UploadFile
from fastapi import FastAPI
from PIL import Image
import io
app = FastAPI()


from starlette.responses import FileResponse 

@app.get("/")
async def read_index():
    return FileResponse('index.html')


@app.post("/analyse")
async def create_upload_file(image: UploadFile):
    img=Image.open(io.BytesIO(await image.read()))
    
    return {"filename": image.filename}