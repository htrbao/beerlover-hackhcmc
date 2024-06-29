from pydantic import BaseModel

class UploadRes(BaseModel):
    """
    "results": {
        "beer_infos": [
            {
                brand: "Heineken 0.0",
                object_type: "Can",
                number: 10,
            },
            {
                brand: "Heineken Silver",
                object_type: "Carton",
                number: 10,
            },
            {
                brand: "Promotion Girl",
                object_type: "Person",
                number: 10,
            },
            //...
            }
        ]
    }
    """
    success: bool
    results: dict