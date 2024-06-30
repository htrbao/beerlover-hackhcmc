from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io

POSM_CLASS = [39]
ID2NAME = {39: 'bottle'}


class BottleDetector:
    def __init__(self, bottle_model_path = "weights/yolov10b.pt", can_model_path = "weights/posm.pt"):
        self.bottle_model = YOLOv10(bottle_model_path)
        self.can_model = YOLOv10(can_model_path)

    def detect(self, numpy_img):
        results = self.bottle_model(numpy_img)
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