from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io
import numpy as np

POSM_CLASS = [0]
ID2NAME = {0: 'person'}

class HumanDetector:
    def __init__(self, model_path = "/home/khoi/Data/YOLO_v10/yolov10/content/best.pt"):
        self.model = YOLOv10(model_path)

    def detect(self, img):
        numpy_img = cv2.imread(img)
        results = self.model(source=numpy_img, conf=0.5)
        person_boxes = [box.xyxy[0].cpu().numpy() for box in results[0].boxes if box.cls == 0]
        confidence_scores = [box.conf[0].cpu().numpy() for box in results[0].boxes if box.cls == 0]
        confidence_scores = np.array(confidence_scores, dtype=np.float32)
        bbox_xyxy = np.array(person_boxes, dtype=np.float32)
        threshold = 0.7
        indices = cv2.dnn.NMSBoxes(bboxes=person_boxes, scores=confidence_scores, score_threshold=0.5, nms_threshold=threshold)
        filtered_boxes = [bbox_xyxy[i] for i in indices.flatten()]
        croped_imgs = []
        for box in filtered_boxes:
            xyxy = list(map(int, box))
            croped_imgs.append(numpy_img[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]])
        croped_base64_imgs = []
        for img in croped_imgs:
            img = Image.fromarray(img)
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            croped_base64_imgs.append(img_str)
        return croped_base64_imgs

