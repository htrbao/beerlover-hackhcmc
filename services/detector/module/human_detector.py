from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io
import numpy as np

POSM_CLASS = [0]
ID2NAME = {0: 'person'}

class HumanDetector:
    def __init__(self, model_path = ""):
        self.model = YOLOv10(model_path)

    def detect_for_prompter(self, img):
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
        return croped_base64_imgs

