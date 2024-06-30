from typing import Optional

from services.beer_vlm.logger import LogManager
from services.beer_vlm.language_model import AbstractLanguageModel
from .abstract_prompter import AbstractPrompter

class FinalPrompter(AbstractPrompter):
    def __init__(self, lm: AbstractLanguageModel, name="final"):
        system_prompt = """
You are expert data analysis.
You are responsible for summaring user provided information with image to give the full details analysis of the image and evaluating the presence of beer based on the number of drinking heineken beer .
This image is usually related to beer in Viet Nam.
All your answer must using all information that user provided. Do not make up any information neither appearing in the image nor in user provided information.
Answer in at most three paragraph. The last paragraph is the evaluation.
        """
        self.final_prompt = """
Summary the image knowing below information and evaluate the presence of beer based on the number of drinking heineken beer in this below list: {heineken_beer}
BACKGROUND: {background}
---END BACKGROUND---
PEOPLE: {person}
---END PEOPLE---
POSM: {posm}
---END POSM---
Answer in English:
"""
        self.heineken_beer = ["Heineken 0.0", "Heineken Silver", "Heineken Sleek", "Tiger Lager", "Tiger Crystal", "Tiger Platinum Wheat Lager", "Tiger Soju Infused Lager", "Edelweiss", "Strongbow", "Larue", "Larue Smooth", "Larue Special", "Bia Việt", "Bivina Lager", "Bivina Export"]
        super(FinalPrompter, self).__init__(lm, system_prompt, name)
        
    def require_prompters(self) ->set[str]:
        require_list = []
        return set(require_list)
    
    async def format_background(self, background):
        if background is None: return ""
        location = background["location"]
        activity = background["activity"]
        atmosphere = background["atmosphere"]
        emotion = background["emotion"]
        return f"image of a {location} with a {', '.join(atmosphere)} atmosphere, evoking feelings of {', '.join(emotion)}, where people are {activity}."
    
    async def format_person(self, person):
        if person is None: return ""
        str_prompt = []
        for p in person:
            str_prompt.append(f"There are {p['number']} of {p['beer_line']}  {p['brand']} people in image.")
        return "\n".join(str_prompt)
    
    async def format_posm(self, posm):
        if posm is None:
            return ""
        str_prompt = []
        for p in posm:
            str_prompt.append(f"There are {p['number']} of {p['beer_line']} {p['brand']} POSM in image.")
        return "\n".join(str_prompt)
            
        
    async def query(self, image: Optional[str], **results) -> str:
        background_prompt = await self.format_background(results.get("background", None))
        person_prompt = await self.format_person(results.get("person", None))
        posm_prompt = await self.format_posm(results.get("posm", None))
        # image showing [number] [object_type] of [list of brands].
        query_prompt = self.final_prompt.format(background=background_prompt, person=person_prompt, posm=posm_prompt, heineken_beer = self.heineken_beer )
        answer = await self.lm.get_response_texts(await self.lm.query(query_prompt, image, 1, self.system_prompt))
        answer = answer[0]
        
        return answer