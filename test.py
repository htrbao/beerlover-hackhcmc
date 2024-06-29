from services.detector.module.posm_detector import PosmDetector
from services.detector.module.bottle_detector import BottleDetector

# posm_detector = PosmDetector()
# print(posm_detector.detect_for_prompter("test_img/1.jpg"))

bottle_detector = BottleDetector("weights/yolov10b.pt")
print(bottle_detector.detect("test_img/2.jpg"))
