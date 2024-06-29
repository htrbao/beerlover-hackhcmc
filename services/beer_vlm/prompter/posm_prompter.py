import backoff
import json
import asyncio
from typing import Optional

from services.beer_vlm.logger import LogManager
from services.beer_vlm.language_model import AbstractLanguageModel
from .abstract_prompter import AbstractPrompter


class POSMPrompter(AbstractPrompter):
    def __init__(self, lm: AbstractLanguageModel, name="posm"):
        system_prompt = """
You are expert in identifying the brand of the point of sales material (POSM) appearing in the image.
All of your answer should be based on the image do not make up anything.
Just answer the brand only.
For brand of beer, you should use the below list of brands if possible.

List of beer brands: Heineken 0.0, Heineken Silver, Heineken Sleek, Tiger Lager, Tiger Crystal, Tiger Platinum Wheat Lager, Tiger Soju Infused Lager, Edelweiss, Strongbow, Larue, Larue Smooth, Larue Special, Bia Việt, Bivina Lager, Bivina Export, Sài gòn, Hà nội, 333, Huda, Trúc Bạch, Budweiser.

Your answer should be in JSON format:
{
    "brand": "brand of posm in the image"
}
        """
        self.posm_prompt = """
There is a POSM in the image. Answer the brand of that POSM in JSON format.
"""

        super(POSMPrompter, self).__init__(lm, system_prompt, name=name)
        
    def require_prompters(self) ->set[str]:
        require_list = []
        return set(require_list)
    
    
    async def default_posm(self):
        return {
            "brand": "unknown",
        }
    
    async def posm_prompt_prepare(self, location="unknown", atmosphere=["neutral"], emotion=["neutral"]):
        return f"image of a {location} with a {', '.join(atmosphere)} atmosphere, evoking feelings of {', '.join(emotion)}"
    
    
    @backoff.on_exception(backoff.expo, exception=Exception,max_time=5, max_tries=2)
    async def handle_posm(self, posm_imgs: list[str], **results) -> dict:
        answers = []
        tasks = []
        for img in posm_imgs:
            task = self.get_answer(img, **results)
            tasks.append(task)
        answers = await asyncio.gather(*tasks)
        return answers
    
    async def get_answer(self, img, **results):
        # answer = await self._get_answer(img, **results)
        try:
            answer = await self._get_answer(img, **results)
        except:
            answer = await self.default_posm()
        return answer
        
    @backoff.on_exception(backoff.expo, exception=Exception,max_time=5, max_tries=2)
    async def _get_answer(self, img, **results):
        query_prompt = self.posm_prompt
        answer = await self.lm.query(query_prompt, img, 1, self.system_prompt)
        answer = await self.lm.get_response_texts(answer)
        answer = answer[0]
        answer = json.loads(answer)
        return answer
        
        
    async def query(self, image: Optional[str], **results) -> str:
        posm_imgs = results.get("posm_images", None)
        if posm_imgs is None:
            return []
        try:
            return await self.handle_posm(posm_imgs, **results)
        except:
            return [await self.default_posm()] * len(posm_imgs)