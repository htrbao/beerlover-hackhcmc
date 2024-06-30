from fastapi import FastAPI, Depends, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import numpy as np
import os
import uuid
import cv2
from PIL import Image
import random
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
from services.detector.module.carton_detector import CartonDetector
from services.detector.module.bottle_detector import BottleDetector
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
        final_bbox = []
        domain = request.base_url

        img = Image.open(file.file).convert("RGB")

        lm = ChatGPT()
        ps_prompter = PersonPrompter(lm)
        bg_prompter = BackgroundPrompter(lm)
        final_prompter = FinalPrompter(lm)
        bg_prompt_executor = PromptExecutor().add_prompter(bg_prompter).build()
        bs_prompt_executor = PromptExecutor().add_prompter(ps_prompter).build()
        final_prompt_executor = PromptExecutor().add_prompter(final_prompter).build()
        
        posmprompter = POSMPrompter(lm)
        posm_prompt_executor = PromptExecutor().add_prompter(posmprompter).build()

        uid = uuid.uuid4()
        main_img_path = os.path.join("services/apis/app/image", f"{uid}.jpg")
        img.save(main_img_path)
        main_img = str(domain) + "image/"  + f"?image_path={uid}.jpg"
            
        human_detector = HumanDetector()
        human_croped_base64_imgs, human_bbox = human_detector.detect(np.asarray(img))
        
        rgb_color = []
        label_color = []
        distinct_color = []
        # print([str(domain) + "image/" +_img for _img in human_croped_base64_imgs])
        bg_task = bg_prompt_executor.execute(main_img)
        ps_task = bs_prompt_executor.execute(main_img, {"person_images": [str(domain) + "image/" +_img for _img in human_croped_base64_imgs]})
        bg_answer, ps_answer = await asyncio.gather(bg_task, ps_task)
        for bbox, brand in zip(human_bbox, ps_answer["person"]):
            tmp = {}
            tmp["box"] = bbox
            tmp['class'] = "Person" + "_" + brand['brand'] + brand['type']
            final_bbox.append(tmp)
            if tmp['class'] not in label_color:
                label_color.append(tmp['class'])
                distinct_color.append([random.randint(0, 255) for _ in range(3)])
            rgb_color.append(distinct_color[label_color.index(tmp['class'])])
        drinker_counter = await count_drinkers(ps_answer["person"])
        # print(drinker_counter)
        
        # carton detect
        carton_detector = CartonDetector()
        carton_croped_base64_imgs, carton_bbox = carton_detector.detect(np.asarray(img))
        carton_results = []
        for carton in carton_croped_base64_imgs:
            brand = recognize_siglip_n_dino(carton)
            carton_results.append(brand)
        for bbox, brand in zip(carton_bbox, carton_results):
            if brand is None: continue
            bbox['box'] = list(map(int, bbox['box'].xyxy.view(-1).tolist()))
            bbox['class'] = str(bbox['class']) + "_" + brand
            final_bbox.append(bbox)
            if bbox['class'] not in label_color:
                label_color.append(bbox['class'])
                distinct_color.append([random.randint(0, 255) for _ in range(3)])
            rgb_color.append(distinct_color[label_color.index(bbox['class'])])
        carton_counter, is_10beer_carton = await count_objects(carton_results, type="Carton")
        
        # bottle detect
        bottle_detector = BottleDetector()
        bottle_croped_base64_imgs, bottle_bbox = bottle_detector.detect(np.asarray(img))
        bottle_results = []
        for bottle in bottle_croped_base64_imgs:
            brand = recognize_siglip_n_dino(bottle)
            bottle_results.append(brand)
        for bbox, brand in zip(bottle_bbox, bottle_results):
            if brand is None: continue
            bbox['box'] = list(map(int, bbox['box'].xyxy.view(-1).tolist()))
            bbox['class'] = str(bbox['class']) + "_" + brand
            final_bbox.append(bbox)
            if bbox['class'] not in label_color:
                label_color.append(bbox['class'])
                distinct_color.append([random.randint(0, 255) for _ in range(3)])
            rgb_color.append(distinct_color[label_color.index(bbox['class'])])
        bottle_counter, is_10beer_bottle = await count_objects(bottle_results, type="Can")
        
        posm_detector = PosmDetector()
        posm_croped_base64_imgs, label_imgs, posm_bbox = posm_detector.detect(np.asarray(img))
        posm_labels = await posm_prompt_executor.execute(None, {"posm_images":  [str(domain) + "image/" +_img for _img in posm_croped_base64_imgs]})
        posm_labels = posm_labels["posm"]
        for bbox, brand in zip(posm_bbox, posm_labels):
            bbox['box'] = list(map(int, bbox['box'].xyxy.view(-1).tolist()))
            bbox['class'] = str(bbox['class']) + "_" + brand['brand']
            final_bbox.append(bbox)
            if bbox['class'] not in label_color:
                label_color.append(bbox['class'])
                distinct_color.append([random.randint(0, 255) for _ in range(3)])
            rgb_color.append(distinct_color[label_color.index(bbox['class'])])
        posm_counter, is_appear = await count_posm(posm_labels, label_imgs)
        
        heineken_presence = is_appear and (is_10beer_carton or is_10beer_bottle)
        final_answer = await final_prompt_executor.execute(main_img, results={
            "background": bg_answer["background"],
            "person": drinker_counter,
            "posm": posm_counter
        })
        
        # print(final_bbox)
        np_img = np.array(img)
        for i, box in enumerate(final_bbox):
            xyxy = box["box"]
            np_img = cv2.rectangle(np_img, (int(xyxy[0]), int(xyxy[1])),(int(xyxy[2]), int(xyxy[3])), rgb_color[i], thickness=5)
        base64_img = Image.fromarray(np_img).convert('RGB')
        buffered = io.BytesIO()
        base64_img.save(buffered, format="JPEG")
        base64_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
        

        return UploadRes(success=True, results={
            "background": bg_answer["background"],
            "beer_person_infos": drinker_counter,
            "beer_carton_infos": carton_counter,
            "beer_can_infos": bottle_counter,
            "beer_posm_infos": posm_counter,
            "description": final_answer["final"],
            "base64_img": base64_img,
            "label_color": label_color,
            "color": distinct_color
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

async def count_objects(objects, type):
    heineken_beer = ["Heineken 0.0", "Heineken Silver", "Heineken Sleek", "Tiger Lager", "Tiger Crystal", "Tiger Platinum Wheat Lager", "Tiger Soju Infused Lager", "Edelweiss", "Strongbow", "Larue", "Larue Smooth", "Larue Special", "Bia Việt", "Bivina Lager", "Bivina Export"]
    is_10beer = False
    counter = defaultdict(int)
    for c in objects:
        counter[c] += 1
    results = []
    
    for brand, v in counter.items():
        if type == "Carton" and brand in heineken_beer and v >= 10:
            is_10beer = True
        results.append({
            "brand": brand,
            "object_type": type,
            "number": v
        })
    return results, is_10beer

async def count_posm(posm, label):
    counter = defaultdict(lambda: defaultdict(int))
    is_standee = False
    is_billboard = False
    for brand, label in zip(posm, label):
        if label == "Standee":
            is_standee = True
        elif label == "Billboard":
            is_billboard = True
        counter[label][brand["brand"]] += 1
    results = []
    
    for type, brand in counter.items():
        for k, v in brand.items():
            results.append({
                "brand": type,
                "beer_line": k,
                "object_type": "POSM",
                "number": v
            })
    return results, (is_standee and is_billboard)