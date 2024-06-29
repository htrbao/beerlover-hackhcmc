from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io
import numpy as np
import uuid
import os
from services.beer_vlm.language_model import ChatGPT
from services.beer_vlm.prompter import *
from services.beer_vlm.logger import LogManager

POSM_CLASS = [0]
ID2NAME = {0: 'carton'}

class CartonDetector:
    def __init__(self, model_path = "weights/carton.pt"):
        self.log_mng = LogManager("test.log", level="debug")
        self.model = YOLOv10(model_path)
        # self.billboard_model = YOLOv10(billboard_model_path)

    def detect(self, numpy_img):
        results = self.model(numpy_img, conf=0.3)
        # billboard_results = self.billboard_model(numpy_img, save=True)
        filtered_boxes_v10 = [{"box": box, "class": ID2NAME[int(box.cls)]} for box in results[0].boxes if box.cls in POSM_CLASS]
        # billboard_results = [{"box": box, "class": "billboard"} for box in billboard_results[0].boxes]
        # filtered_boxes_v10.extend(billboard_results)
        croped_imgs = []
        numpy_img = cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)
        for box in filtered_boxes_v10:
            xyxy = list(map(int, box['box'].xyxy.view(-1).tolist()))
            croped_img = Image.fromarray(numpy_img[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]])

            croped_imgs.append(croped_img)
        # croped_base64_imgs = []
        # for img in croped_imgs:
        #     img = Image.fromarray(img)
        #     buffered = io.BytesIO()
        #     img.save(buffered, format="JPEG")
        #     img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        #     croped_base64_imgs.append(img_str)
        
        return croped_imgs