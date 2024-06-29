from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import faiss

from services.preparations.faiss_helper import read_index
from services.beit3_iir.src import Beit3VisionModel

# from .config import settings
from .dtos import VotingRes

app = FastAPI()
model_beit3 = Beit3VisionModel(device="cpu")

index_beit3, configs_beit3 = read_index("data/faiss-index", "BEiT3.faiss", "BEiT3.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile) -> VotingRes:
    img = Image.open(file.file).convert("RGB")
    xq_b = model_beit3.get_embedding(img)

    D, I = index_beit3.search(xq_b, 5)
    res_beit3 = [configs_beit3[i] for i in I[0]]

    return VotingRes(success=True, results=res_beit3)


