from pathlib import Path
from functools import lru_cache
from typing import Union

import torch
from transformers import AutoProcessor, AutoModel
from PIL import Image

from services.common import VisionModel

CWD = Path(__file__).parent
print(CWD)

class SiglipVisionModel(VisionModel):
    name = "SigLIP"

    def __init__(self, device: str = "cuda"):

        self.model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
        self.processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")
        self.device = device

    def get_embedding(self, input: Image.Image):
        if isinstance(input, Image.Image):
            with torch.no_grad():
                image_input = self.processor(images=input, return_tensors="pt")
                vector = self.model.get_image_features(**image_input)
                norm = vector.norm(dim=-1, keepdim=True)
                vector /= norm
                vector = vector.cpu().detach().numpy().astype("float32")
                return vector
        else:
            raise Exception("Invalid input type")
