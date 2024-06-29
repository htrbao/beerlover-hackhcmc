from PIL import Image
import faiss

from services.preparations.faiss_helper import read_index
from services.dino_iir.src import DinoVisionModel
from services.siglip_iir.src import SiglipVisionModel


model_siglip = SiglipVisionModel(device="cpu")
model_dino = DinoVisionModel(device="cpu")

index_siglip, configs_siglip = read_index("data/faiss-index", "SigLIP.faiss", "SigLIP.json")
index_dino, configs_dino = read_index("data/faiss-index", "Dino.faiss", "Dino.json")

def recognize_siglip_n_dino(img):
    votes = dict()

    xq_s = model_siglip.get_embedding(img)
    xq_d = model_dino.get_embedding(img)

    print("siglip")
    D, I = index_siglip.search(xq_s, 5)
    res_siglip = [configs_siglip[i] for i in I[0]]
    del xq_s

    for id, i in enumerate(I[0]):
        votes[f"{configs_siglip[i]['beer']}_{configs_siglip[i]['type']}"] = {
            "score": D[0][id] * id,
            "config": configs_siglip[i]
        }
        print(configs_siglip[i], D[0][id])

    print("dino")
    D, I = index_dino.search(xq_d, 5)
    res_dino = [configs_dino[i] for i in I[0]]
    del xq_d

    for id, i in enumerate(I[0]):
        votes[f"{configs_dino[i]['beer']}_{configs_dino[i]['type']}"] = {
            "score": D[0][id] * id,
            "config": configs_dino[i]
        }
        print(configs_dino[i], D[0][id])

    return votes