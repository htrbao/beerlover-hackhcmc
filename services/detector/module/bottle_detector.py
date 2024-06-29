from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io

class BottleDetector:
    def __init__(self, model_path = "weights/posm.pt"):
        self.model = YOLOv10(model_path)

    def detect(self, img_path):
        pass