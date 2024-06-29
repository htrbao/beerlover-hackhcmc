from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io
import numpy as np
import os
from services.beer_vlm.language_model import ChatGPT
from services.beer_vlm.prompter import *
from services.beer_vlm.logger import LogManager

POSM_CLASS = [3, 5, 6, 8, 9, 12, 15,17,19]
ID2NAME = {3: 'billboard', 5: 'bucket', 6: 'campain-objects', 8: 'display-stand', 9: 'fridge', 12: 'parasol', 15: 'signage', 17: 'standee', 19: 'tent-card'}

class PosmDetector:
    def __init__(self, model_path = "weights/posm.pt"):
        self.log_mng = LogManager("test.log", level="debug")
        self.model = YOLOv10(model_path)

        self.lm = ChatGPT(log_mng=self.log_mng)
        self.posmprompter = POSMPrompter(self.lm)
        self.prompt_executor = PromptExecutor().add_prompter(self.posmprompter).build()


    async def detect_for_prompter(self, img):
        numpy_img = cv2.imread(img)
        results = self.model(numpy_img)
        filtered_boxes_v10 = [{"box": box, "class": ID2NAME[int(box.cls)]} for box in results[0].boxes if box.cls in POSM_CLASS]
        croped_imgs = []
        for box in filtered_boxes_v10:
            xyxy = list(map(int, box['box'].xyxy.view(-1).tolist()))
            croped_imgs.append(numpy_img[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]])
        croped_base64_imgs = []
        for img in croped_imgs:
            img = Image.fromarray(img)
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            croped_base64_imgs.append(img_str)
        labels = await self.prompt_executor.execute(None, {"posm_images": croped_base64_imgs})
        labels = labels["posm"]
        
        return labels