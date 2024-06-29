import os
from functools import lru_cache
from pathlib import Path
from typing import Union

import torch
from PIL import Image
from timm.data.constants import IMAGENET_INCEPTION_MEAN, IMAGENET_INCEPTION_STD
from timm.models import create_model
from torchvision import transforms
from transformers import XLMRobertaTokenizer

from . import modeling_finetune, utils

# Get current workdir of this file
CWD = Path(__file__).parent
print(CWD)


class Preprocess:
    def __init__(self):
        self.input_size = 384

        self.transform = transforms.Compose(
            [
                transforms.Resize((self.input_size, self.input_size), interpolation=3),
                transforms.ToTensor(),
                transforms.Normalize(mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD),
            ]
        )

    def preprocess(self, input: Image.Image):
        if isinstance(input, Image.Image):
            return self.transform(input).unsqueeze(0)
        else:
            raise Exception("Invalid input type")


class Beit3VisionModel:
    name = "Beit3"
    def __init__(
        self,
        model_name: str = "beit3_base_patch16_384_retrieval",
        model_path: str = os.path.join(
            CWD,
            "beit3_model/beit3_base_patch16_384_coco_retrieval.pth",
        ),
        device: str = "cuda",
    ):
        self._load_model(model_name, model_path, device)
        self.device = device

    # @lru_cache(maxsize=1)
    def _load_model(self, model_name, model_path, device: str = "cpu"):
        self.model = create_model(
            model_name,
            pretrained=False,
            drop_path_rate=0.1,
            vocab_size=64010,
            checkpoint_activations=False,
        )

        self.preprocessor = Preprocess()

        if model_name:
            utils.load_model_and_may_interpolate(model_path, self.model, "model|module", "")
        self.model.to(device)

    def get_embedding(self, input: Union[str, Image.Image]):
        if isinstance(input, Image.Image):
            with torch.no_grad():
                image_input = self.preprocessor.preprocess(input)
                image_input = image_input.to(self.device)
                vector, _ = self.model(image=image_input, only_infer=True)
                norm = vector.norm(dim=-1, keepdim=True)
                vector /= norm
                vector = vector.cpu().detach().numpy().astype("float32")
                return vector
        else:
            raise Exception("Invalid input type")
