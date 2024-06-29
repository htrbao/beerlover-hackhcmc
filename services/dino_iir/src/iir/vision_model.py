from pathlib import Path
from functools import lru_cache
from typing import Union

import torch
from transformers import AutoImageProcessor, AutoModel
from PIL import Image

from services.common import VisionModel

CWD = Path(__file__).parent
print(CWD)

class DinoVisionModel(VisionModel):
    def __init__(self, device: str = "cuda"):
        name_model = "facebook/dinov2-base"
        self.processor = AutoImageProcessor.from_pretrained(name_model)
        self.model = AutoModel.from_pretrained(name_model)
        self.device = device

    def get_embedding(self, input: Image.Image):
        if isinstance(input, Image.Image):
            inputs = self.processor(images=input, return_tensors='pt')
            vector = self.model(**inputs).pooler_output
            vector /= vector.norm(dim=-1, keepdim=True)
            vector = vector.cpu().detach().numpy().astype("float32")
            return vector
        else:
            raise Exception("Invalid input type")

