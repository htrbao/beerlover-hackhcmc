from pathlib import Path
import os
import json

from PIL import Image
import numpy as np
import faiss

from services.common import VisionModel


def write_index(index, index_dir: str = ".", index_name: str = "iir.index"):
    index_path = os.path.join(index_dir, index_name)
    faiss.write_index(index, index_path)


def write_config(config, index_dir: str = ".", config_name: str = "config.json"):
    config_path = os.path.join(index_dir, config_name)
    with open(config_path, "w") as file:
        json.dump(config, file)


def read_index(
    index_dir: str = ".",
    index_name: str = "iir.index",
    config_name: str = "config.json",
):
    index_path = os.path.join(index_dir, index_name)
    config_path = os.path.join(index_dir, config_name)
    index = faiss.read_index(index_path)
    with open(config_path, "r") as file:
        config = json.load(file)
    return index, config


def path_generator(data_src_path: str):
    """
    Generates a path generator for the given data source

    input:
        + data_src_path: path to the data source
    output:
        + beer_name: name of the beer
        + type: type of the image (Carton or bottle)
        + img_path: path to the image
    """
    for beer_path in Path(data_src_path).iterdir():
        beer_dir = str(beer_path).split("/")[-1]
        for type_path in Path(beer_path).iterdir():
            type_dir = str(type_path).split("/")[-1]
            for filename in os.listdir(type_path):
                yield beer_dir, type_dir, os.path.join(type_path, filename)


def make_new_index_for_image_data(
    v_model: VisionModel, data_src_path: str, data_dst_path: str
):
    image_embeddeds = []
    metadatas = []

    for beer, type, img_path in path_generator(data_src_path):
        image = Image.open(img_path).convert("RGB")
        image_embeddeds.append(v_model.get_embedding(image))
        metadatas.append({"beer": beer, "type": type})
        del image
        print(img_path)

    image_embeddeds = np.stack(image_embeddeds).squeeze(axis=1)

    index = faiss.IndexFlatL2(image_embeddeds.shape[-1])
    index.add(image_embeddeds)

    write_index(index, index_dir=data_dst_path, index_name=f"{v_model.name}.faiss")
    write_config(metadatas, index_dir=data_dst_path, config_name=f"{v_model.name}.json")
