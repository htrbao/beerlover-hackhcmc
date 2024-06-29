from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import numpy as np

from PIL import Image
import faiss
import base64
import traceback

from services.preparations.faiss_helper import read_index
from services.dino_iir.src import DinoVisionModel
from services.siglip_iir.src import SiglipVisionModel
from services.beer_vlm.language_model import ChatGPT
from services.beer_vlm.prompter import *
from services.beer_vlm.logger import LogManager
from services.beer_vlm.utils import encode_image

from services.detector.module.posm_detector import PosmDetector
from services.detector.module.human_detector import HumanDetector
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

@app.post("/upload")
async def upload(file: UploadFile) -> UploadRes:
    try:
        img = Image.open(file.file).convert("RGB")

        votes = recognize_siglip_n_dino(img)
        print(votes)
        lm = ChatGPT()
        ps_prompter = PersonPrompter(lm)
        bg_prompter = BackgroundPrompter(lm)
        bg_ps_prompt_executor = PromptExecutor().add_prompter(bg_prompter).add_prompter(ps_prompter).build()
        
        posmprompter = POSMPrompter(lm)
        posm_prompt_executor = PromptExecutor().add_prompter(posmprompter).build()

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        main_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
        human_detector = HumanDetector()
        human_croped_base64_imgs = human_detector.detect(np.asarray(img))
        
        answer = await bg_ps_prompt_executor.execute(main_img, {"person_images": human_croped_base64_imgs})
        print(answer)
        # posm_detector = PosmDetector()
        # posm_croped_base64_imgs = posm_detector.detect("test_img/0.jpg")
        
        # posm_labels = await posm_prompt_executor.execute(None, {"posm_images": posm_croped_base64_imgs})
        # posm_labels = posm_labels["posm"]
        

        return UploadRes(success=True, results={
            "background": answer["background"],
            "person": answer["person"]
        })
    except Exception as e:
        print(traceback.format_exc())
        return UploadRes(success=False, results={"message": str(e)})


