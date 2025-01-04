from starlette.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import base64
from io import BytesIO
from collections import defaultdict
import os
from fastapi import FastAPI
from fastapi import UploadFile, Request, Form
from PIL import Image, ImageDraw, ImageFont
import io
import json
from glob import glob
from datetime import datetime
import threading


import determine
from analyse import analyse
from segment_YOLO import segment_and_separate
from orient_pills import orient_pills



app = FastAPI()

server_session_state = defaultdict(dict)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def read_machine(mid):
    """Lese die Konfigurationsdatei der Maschine 

    Args:
        mid (int): ID der Maschine 

    Returns:
        dict: Konfiguration der Maschine
    """
    try:
        with open(f"machines/{mid}.json", encoding="UTF-8")as f:
            return json.load(f)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError:
        raise


def write_machine(mid, config):
    """Schreibt die Maschinenkonfigdatei

    Args:
        mid (int): ID der Maschine
        config (dict): Konfiguration der Maschine
    """
    with open(f"machines/{mid}.json", "w", encoding="UTF-8")as f:
        json.dump(config, f)


@app.get("/preview", name="preview")
def preview(tablette: str):
    return FileResponse(glob(f"classify_data/{tablette}/*")[0])


@app.get("/config/{mid}")
def config(request: Request, mid: int):
    with open("pills_in_sample.json")as f:
        pills_in_sample=json.load(f)
    return templates.TemplateResponse('config.html',
            context={
                "request": request,
                "mid": mid,
                "config": read_machine(mid),
                "num_cols": len(read_machine(mid)["plaene"])+1,
                "pills_in_sample":pills_in_sample["list"],
                "match":pills_in_sample["match"]
                })


@app.get("/config/{mid}/update")
def update(request: Request, mid: int, time: str, tablette: str, value: int):
    machine = read_machine(mid)
    machine["plaene"][time][tablette] = value
    write_machine(mid, machine)
    return {}


@app.get("/config/{mid}/add")
def add_pill(request: Request,  mid: int, name: str | None = None):
    """Funktion, die neue Tablette anlegt

    Args:
        request (Request): Anfrage
        mid (int): ID der Maschine
        name (str | None, optional): Name der Tablette

    Returns:
        TemplateResponse|RedirectResponse: Antwort an den Client
    """
    global server_session_state
    if (not "add_imgs" in server_session_state[mid].keys()) and (name not in os.listdir("classify_data")):
        name = ""
    if name:
        if (name not in os.listdir("classify_data")):
            os.mkdir(f"classify_data/{name}")
            for i, img in enumerate(server_session_state[mid]["add_imgs"]):
                img.save(f"classify_data/{name}/{i}.png")
        config = read_machine(mid)
        config["tabletten"].append(name)
        write_machine(mid, config)
        server_session_state[mid]["add"] = False
        server_session_state[mid]["add_imgs"] = []
        threading.Thread(target=determine.reload).start()
        return RedirectResponse(f"/config/{mid}")

    server_session_state[mid]["add"] = True
    return templates.TemplateResponse('add_pill.html', context={"request": request, "mid": mid, "existing_pills": os.listdir("classify_data"), "config": read_machine(mid)})


@app.get("/config/{mid}/add/get_imgs")
def get_added_imgs(request: Request, mid: int):
    global server_session_state
    ret = [] #return-Value Data-URI 

    for img in server_session_state[mid].get("add_imgs", []):
        buffered = BytesIO()
        img.resize((100, 100)).save(buffered, format="JPEG")
        img_str = "data:image/jpeg;base64," + \
            base64.b64encode(buffered.getvalue()).decode("utf-8")
        ret.append(img_str)

    return ret


def handle_add_pill_file_upload(img, mid):
    """fügt ein Bild in eine Liste im RAM hinzu wird verwendet um neue Tabletten anzulegen

    Args:
        img (Image.Image): Neues Bild von einer Tablette 
        mid (int): ID der Maschine
    """
    if not "add_imgs" in server_session_state[mid].keys():
        server_session_state[mid]["add_imgs"] = []
    server_session_state[mid]["add_imgs"] += orient_pills(
        segment_and_separate(img))


@app.get("/config/{mid}/add/delete_img")
def remove_add_pill_image(mid: int, img: int):
    server_session_state[mid]["add_imgs"].pop(img)


font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", 20)


def get_current_plan(mid):
    """Liest den aktuellen Medikamentenplan basierend auf der Uhrzeit ein.

    Args:
        mid (int): Maschinen-ID

    Returns:
        dict[str:int]: Medikamentenplan für die aktuelle Uhrzeit
    """
    machine = read_machine(mid)
    plan=machine["plaene"][min(machine["plaene"],
                                 key=lambda t: abs(
                                     (int(t.split(":")[0]) *
                                      60+int(t.split(":")[1]))
                                     -
                                     (datetime.now().hour*60+datetime.now().minute)
    ))]
    plan={k:v for k,v in plan.items() if v!=0}
    return plan

@app.post("/analyse")
def analyse_endpoint(image: UploadFile, mid: int = Form()):
    """Client lädt Bild hoch

    Args:
        image (Image.Image): Bild mit Tabletten(mix)
        mid (int): ID der Maschine

    Returns:
        dict: Antwort: Name der Tabletten und Übereinstimmung mit Medikamentenplan
    """
    img = Image.open(io.BytesIO(image.file.read()))
    img.save("static/orig_image.png")
    if server_session_state[mid].get("add", False):
        handle_add_pill_file_upload(img, mid)
        return {"pills": {}, "match": True, "status": 200}
    types = []
    pills_in_sample = analyse(img, options=read_machine(mid)[
                              "tabletten"], types=types)
    out_img = Image.new("RGB", (int((img.height/8)*len(types)), int(img.height/8)),(255,255,255))
    for i in range(sum(pills_in_sample.values())):
        out_img.paste(Image.open(f"{i}.png").resize(
            (int(img.height/8), int(img.height/8))), (int(img.height/8)*i, 0))
    draw = ImageDraw.Draw(out_img)
    for i, name in enumerate(types):
        draw.text((int(img.height/8)*(i), 0),
                  name, (255, 255, 255), align="center")
    out_img.save("static/img.png")
    
    with open("pills_in_sample.json","w")as f:
        json.dump({"list":types,"match":pills_in_sample == get_current_plan(mid)},f)
    return {"pills": pills_in_sample, "match": pills_in_sample == get_current_plan(mid)}
