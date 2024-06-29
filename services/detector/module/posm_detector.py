from ultralytics import YOLOv10
import supervision as sv
from PIL import Image

POSM_CLASS = [3, 5, 6, 8, 9, 12, 15,17,19]
ID2NAME = {3: 'billboard', 5: 'bucket', 6: 'campain-objects', 8: 'display-stand', 9: 'fridge', 12: 'parasol', 15: 'signage', 17: 'standee', 19: 'tent-card'}
def posm_detection(img_path):
    model = YOLOv10('./data/model/posm.pt')

    img = Image.open(img_path).convert('RGB')
    results = model(img, show=True)
    filtered_boxes_v10 = [{"box": box, "class": ID2NAME[int(box.cls)]} for box in results[0].boxes if box.cls in POSM_CLASS]
    return filtered_boxes_v10

