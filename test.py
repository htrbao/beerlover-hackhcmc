import os
import asyncio

from services.detector.module.posm_detector import PosmDetector
from services.detector.module.bottle_detector import BottleDetector

# posm_detector = PosmDetector()
# print(posm_detector.detect("test_img/1.jpg"))

# detector = PosmDetector()
# answer = asyncio.run(detector.detect("test_img/0.jpg"))

bottle = BottleDetector()
answer = bottle.detect("test_img/3.jpg")

print(answer)