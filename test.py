import os
import asyncio

from services.detector.module.posm_detector import PosmDetector




detector = PosmDetector()
answer = asyncio.run(detector.detect_for_prompter("test_img/1.jpg"))

print(answer)