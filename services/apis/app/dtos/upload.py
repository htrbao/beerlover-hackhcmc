from pydantic import BaseModel

class UploadRes(BaseModel):
    """
    "results": {
        "beer_can_infos": [
            {
                brand: "Heineken 0.0",
                object_type: "Can",
                number: 10,
            },
            
        ],
        "beer_carton_infos": [
            {
                brand: "Heineken Silver",
                object_type: "Carton",
                number: 10,
            },
        ],
        "beer_person_infos": [
            {
                brand: "Promotion Girl",
                beer_line: "Heineken 0.0",
                object_type: "Person",
                number: 10,
            },
        ],
        "background": {
            'location': 'street restaurant', 
            'activity': 'dining', 
            'atmosphere': ['casual', 'welcoming', 'bustling'], 
            'emotion': ['relaxed', 'social', 'content']
        }
    }
    """
    success: bool
    results: dict