from fastapi import FastAPI, Depends, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import numpy as np
import os

from PIL import Image
import faiss
import base64
import traceback
import asyncio
from services.preparations.faiss_helper import read_index
from services.dino_iir.src import DinoVisionModel
from services.siglip_iir.src import SiglipVisionModel
from services.beer_vlm.language_model import ChatGPT
from services.beer_vlm.prompter import *
from services.beer_vlm.logger import LogManager
from services.beer_vlm.utils import encode_image

from services.detector.module.posm_detector import PosmDetector
from services.detector.module.human_detector import HumanDetector
from collections import defaultdict
import io
# from .config import settings
from .dtos import UploadRes
from ..utils import recognize_siglip_n_dino

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)
# log_mng = LogManager("test.log", level="debug")

@app.post("/upload")
async def upload(file: UploadFile, request: Request) -> UploadRes:
    # global log_mng
    try:
        domain = request.base_url
        beer_can_infos =[]
        beer_carton_infos =[]
        beer_person_infos =[]
        img = Image.open(file.file).convert("RGB")

        votes = recognize_siglip_n_dino(img)
        print(votes)
        lm = ChatGPT()
        ps_prompter = PersonPrompter(lm)
        bg_prompter = BackgroundPrompter(lm)
        bg_prompt_executor = PromptExecutor().add_prompter(bg_prompter).build()
        bs_prompt_executor = PromptExecutor().add_prompter(ps_prompter).build()
        
        
        # posmprompter = POSMPrompter(lm)
        # posm_prompt_executor = PromptExecutor().add_prompter(posmprompter).build()

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        main_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
        human_detector = HumanDetector()
        human_croped_base64_imgs = human_detector.detect(np.asarray(img))
        
        print([str(domain) + "image/" +_img for _img in human_croped_base64_imgs])
        bg_task = bg_prompt_executor.execute(main_img)
        ps_task = bs_prompt_executor.execute(main_img, {"person_images": [str(domain) + "image/" +_img for _img in human_croped_base64_imgs]})
        bg_answer, ps_answer = await asyncio.gather(bg_task, ps_task)
        drinker_counter = await count_drinkers(ps_answer["person"])
        print(drinker_counter)
        # posm_detector = PosmDetector()
        # posm_croped_base64_imgs = posm_detector.detect("test_img/0.jpg")
        
        # posm_labels = await posm_prompt_executor.execute(None, {"posm_images": posm_croped_base64_imgs})
        # posm_labels = posm_labels["posm"]
        

        return UploadRes(success=True, results={
            "background": bg_answer["background"],
            "beer_person_infos": drinker_counter
        })
    except Exception as e:
        print(traceback.format_exc())
        return UploadRes(success=False, results={"message": str(e)})
    
@app.get("/image/")
async def get_image(image_path: str):
    image_path = os.path.join("services/apis/app/image", image_path)
    if os.path.exists(image_path) and os.path.isfile(image_path):
        return FileResponse(image_path, media_type="image/jpeg")
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
# problem 1 counting drinker
async def count_drinkers(person):
    counter = defaultdict(lambda: defaultdict(int))
    for p in person:
        counter[p["type"]][p["brand"]] += 1
    results = []
    
    for type, brand in counter.items():
        for k, v in brand.items():
            results.append({
                "brand": type,
                "beer_line": k,
                "object_type": "Person",
                "number": v
            })
    return results