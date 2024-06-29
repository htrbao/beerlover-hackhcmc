from services.detector.module.posm_detector import PosmDetector

detector = PosmDetector()
print(detector.detect_for_prompter("test_img/1.jpg"))
