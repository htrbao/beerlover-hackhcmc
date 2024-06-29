import backoff
import json
import time
import asyncio
from typing import Optional

from services.beer_vlm.logger import LogManager
from services.beer_vlm.language_model import AbstractLanguageModel
from .abstract_prompter import AbstractPrompter


class PersonPrompter(AbstractPrompter):
    def __init__(self, lm: AbstractLanguageModel, name="person"):
        system_prompt = """
You are expert in identifying the type of the person appearing in the image knowing its location.
All of your answer should be based on the image do not make up anything.

You only need to be choose a single type of person from this list of type: Promotion, Buyer, Seller, Drinker, Staff.

If that person is Promotion or Drinker you will be choose the brand of the used or promoted beer from this list of beer brands: Heineken 0.0, Heineken Silver, Heineken Sleek, Tiger Lager, Tiger Crystal, Tiger Platinum Wheat Lager, Tiger Soju Infused Lager, Edelweiss, Strongbow, Larue, Larue Smooth, Larue Special, Bia Việt, Bivina Lager, Bivina Export, Sài gòn, Hà nội, 333, Huda, Trúc Bạch, Budweiser. Otherwise, just answer that brand is "Other beverage" or "Not drinking".

Your answer should be in JSON format:
{
    "type": "the type of that person",
    "brand": "brand if possible else other beverage"
}
        """
        self.person_prompt = """
There is a person in the image at {location} location. Answer the type of that person and brand of that person in JSON format.
"""

        super(PersonPrompter, self).__init__(lm, system_prompt, name=name)
        
    def require_prompters(self) ->set[str]:
        require_list = []
        return set(require_list)
    
    
    async def default_person(self):
        return {
            "type": "Customer",
            "brand": "Other beverage",
        }
    
    async def person_prompt_prepare(self, type="Customer", brand="other beverage"):
        return f"image of a {type} with {brand}"
    
    @backoff.on_exception(backoff.expo, exception=Exception,max_time=5, max_tries=2)
    async def handle_person(self, main_image, person_imgs: list[str], **results) -> dict:
        answers = []
        tasks = []
        for img in person_imgs:
            task = self.get_answer(img, main_image, **results)
            tasks.append(task)
        answers = await asyncio.gather(*tasks)
        return answers
    
    async def get_answer(self, img, main_image, **results):
        # answer = await self._get_answer(img, main_image, **results)
        try:
            answer = await self._get_answer(img, main_image, **results)
        except:
            answer = await self.default_person()
        return answer
        
    @backoff.on_exception(backoff.expo, exception=Exception,max_time=5, max_tries=2)
    async def _get_answer(self, img, main_image, **results):
        query_prompt = self.person_prompt.format(location=results.get("background", {}).get("location", ""))
        answer = await self.lm.query(query_prompt, img, 1, self.system_prompt, main_image=main_image)
        answer = await self.lm.get_response_texts(answer)
        answer = answer[0]
        answer = json.loads(answer)
        
        return answer
        
    async def query(self, image: Optional[str], **results) -> str:
        person_imgs = results.get("person_images", None)
        if person_imgs is None:
            return []
        try:
            return await self.handle_person(image, person_imgs, **results)
        except:
            return [await self.default_person()] * len(person_imgs)