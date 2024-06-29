from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io

class BottleDetector:
    def __init__(self, bottle_model_path = "weights/yolov10b.pt", can_model_path = "weights/posm.pt"):
        self.bottle_model = YOLOv10(bottle_model_path)
        self.can_model = YOLOv10(can_model_path)

    def detect(self, img_path):
        numpy_img = cv2.imread(img_path)
        results = self.model(numpy_img, save=True, classes=["bottle"])