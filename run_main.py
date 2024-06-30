from services.detector.module.merge_carton_detector import MergeCartonDetector 
from ultralytics import YOLOv10
import cv2
import numpy as np
import matplotlib.pyplot as plt
from services.apis.utils import recognize_siglip_n_dino

model_path = "/home/khoi/Data/YOLO_v10/yolov10/content/best.pt"
image_path = "/home/khoi/Data/YOLO_v10/beerlover-hackhcmc/66500954_1707307474952.jpg"
image = cv2.imread(image_path)
mer_element = MergeCartonDetector(model_path)
filtered_boxes = mer_element.bbox_output(image)
print(filtered_boxes)
# dictionary = {}
# for box in filtered_boxes:
#     x1, y1, x2, y2 = map(int, box)
#     crop_roi = image[y1:y2, x1:x2] 
#     beer_label = recognize_siglip_n_dino(crop_roi)
#     if beer_label not in dictionary.keys():
#         dictionary[beer_label] = [x1, y1, x2, y2]
#     else:
#         if x1 < dictionary[beer_label][0]:
#             dictionary[beer_label][0] = x1
#         if y1 < dictionary[beer_label][1]:
#             dictionary[beer_label][1] = y1
#         if x2 > dictionary[beer_label][2]:
#             dictionary[beer_label][2] = x2
#         if y2 > dictionary[beer_label][3]:
#             dictionary[beer_label][3] = y2

# print(dictionary)







