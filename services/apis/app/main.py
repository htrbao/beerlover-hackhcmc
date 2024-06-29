from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import faiss

from services.preparations.faiss_helper import read_index
from services.dino_iir.src import DinoVisionModel
from services.siglip_iir.src import SiglipVisionModel

# from .config import settings
from .dtos import UploadRes
from ..utils import recognize_siglip_n_dino

app = FastAPI()
model_siglip = SiglipVisionModel(device="cpu")
model_dino = DinoVisionModel(device="cpu")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile) -> UploadRes:
    try:
        img = Image.open(file.file).convert("RGB")

        votes = recognize_siglip_n_dino(img)
        print(votes)

        return UploadRes(success=True, results={})
    except Exception as e:
        return UploadRes(success=False, results={"message": str(e)})


