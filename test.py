import os
import asyncio

from services.detector.module.posm_detector import PosmDetector
from services.detector.module.human_detector import HumanDetector





# detector = PosmDetector()
detector = HumanDetector()
answer = asyncio.run(detector.detect_for_prompter("test_img/1.jpg"))

print(answer)