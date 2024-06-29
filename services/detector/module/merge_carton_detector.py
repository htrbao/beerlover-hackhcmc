from ultralytics import YOLOv10
import cv2
import numpy as np
import matplotlib.pyplot as plt
from services.apis.utils import recognize_siglip_n_dino
from PIL import Image


class MergeCartonDetector:
    def __init__(self, model_path = "/home/khoi/Data/YOLO_v10/yolov10/content/best.pt"):
        self.model = YOLOv10(model_path)
    
    def bbox_output(self,image):
        image_copy=image.copy()
        results = self.model(source=image, conf=0.6)
        person_boxes = [box.xyxy[0].cpu().numpy() for box in results[0].boxes if box.cls == 0]
        confidence_scores = [box.conf[0].cpu().numpy() for box in results[0].boxes if box.cls == 0]
        confidence_scores = np.array(confidence_scores, dtype=np.float32)
        bbox_xyxy = np.array(person_boxes, dtype=np.float32)
        image_pil = Image.fromarray(image_copy)
        dictionary = {}
        for box in bbox_xyxy:
            x1, y1, x2, y2 = box
            crop_roi = image_pil.crop((x1, y1, x2, y2)) 
            beer_label = recognize_siglip_n_dino(crop_roi)
            # print(beer_label)
            if dictionary.get(beer_label) is None:
                dictionary[beer_label] = [x1, y1, x2, y2]
            else:
                if x1 < dictionary[beer_label][0]:
                    dictionary[beer_label][0] = x1
                if y1 < dictionary[beer_label][1]:
                    dictionary[beer_label][1] = y1
                if x2 > dictionary[beer_label][2]:
                    dictionary[beer_label][2] = x2
                if y2 > dictionary[beer_label][3]:
                        dictionary[beer_label][3] = y2

        i = 20
        for bbox in dictionary.values():
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(image_copy, (x1, y1), (x2, y2), (0, 255-i, 0), 2)  # Green box with thickness 2
            i+=10        
        # Convert BGR image to RGB
        image_copy_rgb = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
        
        # Display the image with bounding boxes using plt
        plt.figure(figsize=(10, 10))
        plt.imshow(image_copy_rgb)
        plt.axis('off')  # Hide axes
        plt.show()
        exit()
        return dictionary

    # print(dictionary)



    # # Display the image
    # # for xmin, ymin, xmax, ymax in filtered_boxes:
    # #     cv2.rectangle(image_copy, (xmin, ymin), (xmax, ymax), (0, 0, 255), 3)


