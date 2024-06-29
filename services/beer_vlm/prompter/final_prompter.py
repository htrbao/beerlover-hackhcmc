from typing import Optional

from services.beer_vlm.logger import LogManager
from services.beer_vlm.language_model import AbstractLanguageModel
from .abstract_prompter import AbstractPrompter

class FinalPrompter(AbstractPrompter):
    def __init__(self, lm: AbstractLanguageModel, name="final"):
        system_prompt = """
You are expert in describing the image.
This image is usually related to beer in Viet Nam.
You are responsible for summaring user provided information with image to give the full details analysis of the image.
All your answer must using all information that user provided. Do not make up any information neither appearing in the image nor in user provided information.
Answer in at most three paragraph.
        """
        self.final_prompt = """
Summary the image knowing below information
BACKGROUND: {background}
---END BACKGROUND---
Answer in English:
"""
        super(FinalPrompter, self).__init__(lm, system_prompt, name)
        
    def require_prompters(self) ->set[str]:
        require_list = ["background"]
        return set(require_list)
        
    async def query(self, image: Optional[str], **results) -> str:
        return "Example"
        query_prompt = self.final_prompt.format(background=results.get("background", "").get("prompt", ""))
        answer = await self.lm.get_response_texts(await self.lm.query(query_prompt, image, 1, self.system_prompt))
        answer = answer[0]
        
        return answer