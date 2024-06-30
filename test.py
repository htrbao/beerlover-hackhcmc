import os
import asyncio

from services.detector.module.posm_detector import PosmDetector
from services.detector.module.bottle_detector import BottleDetector
from services.detector.module.human_detector import HumanDetector


detector = PosmDetector()
answer = asyncio.run(detector.detect("test_img/4.jpg"))

<<<<<<< HEAD
# bottle = BottleDetector()
# answer = bottle.detect("test_img/3.jpg")
=======

# detector = PosmDetector()
detector = HumanDetector()
answer = asyncio.run(detector.detect_for_prompter("test_img/2.jpg"))
>>>>>>> 988eb64d1fd26edd97342a91fd360085550352df

print(answer)