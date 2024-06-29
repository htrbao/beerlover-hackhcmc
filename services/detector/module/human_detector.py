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
from services.beer_vlm.utils import encode_image

POSM_CLASS = [0]
ID2NAME = {0: 'person'}

class HumanDetector:
    def __init__(self,  model_path = "weights/yolov10b.pt"):
        self.log_mng = LogManager("test.log", level="debug")
        self.model = YOLOv10(model_path)

        self.lm = ChatGPT(log_mng=self.log_mng)
        self.ps_prompter = PersonPrompter(self.lm)
        self.prompt_executor = PromptExecutor().add_prompter(self.ps_prompter).build()


    async def detect_for_prompter(self, img):
        numpy_img = cv2.imread(img)
        results = self.model(numpy_img, classes=POSM_CLASS, conf=0.5, save=True)
        filtered_boxes_v10 = [{"box": box, "class": ID2NAME[int(box.cls)]} for box in results[0].boxes if box.cls in POSM_CLASS]
        croped_imgs = []
        for box in filtered_boxes_v10:
            xyxy = list(map(int, box['box'].xyxy.view(-1).tolist()))
            croped_imgs.append(numpy_img[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]])
        croped_base64_imgs = []
        for _img in croped_imgs:
            _img = Image.fromarray(_img)
            buffered = io.BytesIO()
            _img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            croped_base64_imgs.append(img_str)
        img = Image.fromarray(numpy_img)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        main_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        labels = await self.prompt_executor.execute(main_img, {"person_images": croped_base64_imgs})
        labels = labels["person"]
        
        return labels

