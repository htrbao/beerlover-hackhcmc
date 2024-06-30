from PIL import Image
import faiss

from services.preparations.faiss_helper import read_index
from services.dino_iir.src import DinoVisionModel
from services.siglip_iir.src import SiglipVisionModel
from services.beit3_iir.src import Beit3VisionModel


model_siglip = SiglipVisionModel(device="cuda")
model_dino = DinoVisionModel(device="cuda")
model_beit3 = Beit3VisionModel(device="cuda")

index_siglip, configs_siglip = read_index("data/faiss-index", "SigLIP.faiss", "SigLIP.json")
index_dino, configs_dino = read_index("data/faiss-index", "Dino.faiss", "Dino.json")
index_beit3, configs_beit3 = read_index("data/faiss-index", "Beit3.faiss", "Beit3.json")

def recognize_siglip_n_dino(img):
    votes = dict()

    xq_s = model_siglip.get_embedding(img)
    # xq_d = model_dino.get_embedding(img)
    xq_b = model_beit3.get_embedding(img)

    D, I = index_siglip.search(xq_s, 5)
    del xq_s

    for id, i in enumerate(I[0]):
        if D[0][id] < 0.45:
            continue
        if configs_siglip[i]['beer'] in votes.keys():
            votes[f"{configs_siglip[i]['beer']}"] += D[0][id] * (id + 1)
        else:
            votes[f"{configs_siglip[i]['beer']}"] = D[0][id] * (id + 1)
        # print(configs_siglip[i], D[0][id])

    # D, I = index_dino.search(xq_d, 5)
    # del xq_d

    # for id, i in enumerate(I[0]):
    #     if D[0][id] < 0.45:
    #         continue
    #     if configs_dino[i]['beer'] in votes.keys():
    #         votes[f"{configs_dino[i]['beer']}"] += D[0][id] * (id + 1)
    #     else:
    #         votes[f"{configs_dino[i]['beer']}"] = D[0][id] * (id + 1)
    #     print(configs_dino[i], D[0][id])

    D, I = index_beit3.search(xq_b, 5)
    del xq_b

    for id, i in enumerate(I[0]):
        if D[0][id] < 0.45:
            continue
        if configs_beit3[i]['beer'] in votes.keys():
            votes[f"{configs_beit3[i]['beer']}"] += D[0][id] * (id + 1)
        else:
            votes[f"{configs_beit3[i]['beer']}"] = D[0][id] * (id + 1)
        # print(configs_beit3[i], D[0][id])

    predict_class = None
    for k, v in votes.items():
        if predict_class is None or v > votes[predict_class]:
            predict_class = k

    return predict_class