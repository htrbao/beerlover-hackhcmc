import backoff
import json
import asyncio
from typing import Optional

from beer_vlm.logger import LogManager
from beer_vlm.language_model import AbstractLanguageModel
from .abstract_prompter import AbstractPrompter


class BillboardPrompter(AbstractPrompter):
    def __init__(self, lm: AbstractLanguageModel, name="billboard"):
        system_prompt = """
You are expert in identifying the brand of the billboard appearing in the image.
All of your answer should be based on the image do not make up anything.
Just answer the brand only.
For brand of beer, you should use the below list of brands if possible.

List of beer brands: Heineken 0.0, Heineken Silver, Heineken Sleek, Tiger Lager, Tiger Crystal, Tiger Platinum Wheat Lager, Tiger Soju Infused Lager, Edelweiss, Strongbow, Larue, Larue Smooth, Larue Special, Bia Việt, Bivina Lager, Bivina Export, Sài gòn, Hà nội, 333, Huda, Trúc Bạch, Budweiser.

Your answer should be in JSON format:
{
    "brand": "brand of billboard in the image"
}
        """
        self.billboard_prompt = """
There is a billboard in the image. Answer the brand of that billboard in JSON format.
"""

        super(BillboardPrompter, self).__init__(lm, system_prompt, name=name)
        
    def require_prompters(self) ->set[str]:
        require_list = []
        return set(require_list)
    
    
    async def default_billboard(self):
        return {
            "brand": "unknown",
        }
    
    async def billboard_prompt_prepare(self, location="unknown", atmosphere=["neutral"], emotion=["neutral"]):
        return f"image of a {location} with a {', '.join(atmosphere)} atmosphere, evoking feelings of {', '.join(emotion)}"
    
    
    @backoff.on_exception(backoff.expo, exception=Exception,max_time=5, max_tries=2)
    async def handle_billboard(self, billboard_imgs: list[str], **results) -> dict:
        answers = []
        tasks = []
        for img in billboard_imgs:
            task = self.get_answer(img, **results)
            tasks.append(task)
        answers = await asyncio.gather(*tasks)
        return answers
    
    async def get_answer(self, img, **results):
        # answer = await self._get_answer(img, **results)
        try:
            answer = await self._get_answer(img, **results)
        except:
            answer = await self.default_billboard()
        return answer
        
    @backoff.on_exception(backoff.expo, exception=Exception,max_time=5, max_tries=2)
    async def _get_answer(self, img, main_image, **results):
        query_prompt = self.billboard_prompt
        answer = await self.lm.query(query_prompt, img, 1, self.system_prompt, main_image=main_image)
        answer = await self.lm.get_response_texts(answer)
        answer = answer[0]
        answer = json.loads(answer)
        return answer
        
        
    async def query(self, image: Optional[str], **results) -> str:
        billboard_imgs = results.get("billboard_images", None)
        if billboard_imgs is None:
            return []
        try:
            return await self.handle_billboard(billboard_imgs, **results)
        except:
            return [await self.default_billboard()] * len(billboard_imgs)