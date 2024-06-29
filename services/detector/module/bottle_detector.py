from ultralytics import YOLOv10
from PIL import Image
import cv2
import base64
import io

class BottleDetector:
    def __init__(self, bottle_model_path = "weights/yolov10b.pt", can_model_path = "weights/can_yolov10s.pt"):
        self.bottle_model = YOLOv10(bottle_model_path)
        self.can_model = YOLOv10(can_model_path)

    def detect(self, img_path):
        numpy_img = cv2.imread(img_path)
        results = self.bottle_model(numpy_img, classes=[39], conf=0.5)
        can_window = 150
        for i in range(numpy_img.shape[0] // can_window):
            for j in range(numpy_img.shape[1] // can_window):
                can = numpy_img[i * can_window:(i + 1) * can_window, j * can_window:(j + 1) * can_window, :]
                can_results = self.can_model(can, save=True, conf=0.7)
                print(can_results)
                if len(can_results[0].boxes) > 0:
                    for box in can_results[0].boxes:
                        xyxy = list(map(int, box.xyxy.view(-1).tolist()))
                        # draw bbox rectangle
                        can = cv2.rectangle(
                            can,
                            (xyxy[0], xyxy[1]),
                            (xyxy[2], xyxy[3]),
                            (0, 0, 255),
                            3,
                            cv2.LINE_AA,
                        )
                    print(can.shape)
                    cv2.imshow("can", can)
                    cv2.waitKey(0)