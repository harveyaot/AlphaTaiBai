import shutil
import os
import torch
import requests

from typing import List
from tempfile import NamedTemporaryFile
from pathlib import Path

from torchvision import transforms
from typing import Union
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageOps

from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel, parse_obj_as

class Item(BaseModel):
    sent: str
    source: str
    score:float


app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"Hello_world": "Stock:v3.2"}


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/v6/finance/quote')
async def stock(region: str | None, lang: str | None, symbols: str, req: Request):
    headers = {'x-api-key': 'avvsCXpRI1abGc3JPraDP2XEPYe0FYr05D3CUfIA'}
    params = {'region': region, 'lang': lang, 'symbols': symbols}
    base_url = "https://yfapi.net/v6/finance/quote"
    t_resp = requests.get(base_url, params=params, headers=headers)
    response = Response(content=t_resp.content,
                        status_code=t_resp.status_code, media_type="application/json")
    return response

def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
        tmp_path = Path(tmp.name)
        print(tmp_path)
    finally:
        upload_file.file.close()
    return tmp_path


@app.post("/uploadfile")
async def create_upload_file(file:UploadFile):
    try:
        tmp_path = save_upload_file_tmp(file)
        pil = Image.open(tmp_path).convert('RGB')
        pil = ImageOps.exif_transpose(pil)
        #print(pil.size)
        pil = transforms.Resize(500)(pil)
        pil = transforms.CenterCrop((480, 420))(pil)
        pil.save('./uploads/' + file.filename)
        #print(tmp_path)
        os.remove(tmp_path)
    finally:
        file.file.close()
    return {"filename": file.filename}

from .ImageCLF import get_transforms, inference, ImageClf18

model = ImageClf18()
model_path = "./checkpoint.pt"
best_checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
model.load_state_dict(best_checkpoint["state_dict"])
model.eval()

@app.get("/imageclf", response_model=Page[Item])
async def imageclf(filename:str):
    if filename.startswith('/static'):
        predicts = inference(model, "." + filename, 200)
    else:
        predicts = inference(model, "./uploads/" + filename, 200)
    res = parse_obj_as(List[Item], predicts)
    return paginate(res)

# Register
add_pagination(app)
    