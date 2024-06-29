from functools import lru_cache
from typing import Union

import clip
from PIL import Image
from torchvision import transforms


class VisionModel:
    name = "CLIP"

    def __init__(self, model_name: str = "ViT-B/32", device: str = "cuda"):
        self._load_model(model_name, device)
        self.device = device

    @lru_cache(maxsize=1)
    def _load_model(self, model_name, device: str = "cpu"):
        self.model, self.processor = clip.load(model_name, device=device)

    def get_embedding(self, input: Image.Image):
        if isinstance(input, Image.Image):
            image_input = self.processor(input).unsqueeze(0).to(self.device)
            vector = self.model.encode_image(image_input)
            vector /= vector.norm(dim=-1, keepdim=True)
            vector = vector.cpu().detach().numpy().astype("float32")
            return vector
        else:
            raise Exception("Invalid input type")
