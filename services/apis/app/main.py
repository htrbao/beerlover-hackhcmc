from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import faiss

from services.preparations.faiss_helper import read_index
from services.dino_iir.src import DinoVisionModel
from services.siglip_iir.src import SiglipVisionModel

# from .config import settings
from .dtos import UploadRes

app = FastAPI()
model_siglip = SiglipVisionModel(device="cpu")
model_dino = DinoVisionModel(device="cpu")

index_siglip, configs_siglip = read_index(
    "data/faiss-index", "SigLIP.faiss", "SigLIP.json"
)
index_dino, configs_dino = read_index("data/faiss-index", "Dino.faiss", "Dino.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile) -> UploadRes:
    img = Image.open(file.file).convert("RGB")
    xq_s = model_siglip.get_embedding(img)
    xq_d = model_dino.get_embedding(img)

    D, I = index_siglip.search(xq_s, 5)
    res_siglip = [configs_siglip[i] for i in I[0]]
    D, I = index_dino.search(xq_d, 5)
    res_dino = [configs_dino[i] for i in I[0]]

    return UploadRes(success=True, results=[*res_siglip, *res_dino])


