import abc
from typing import Optional

from beer_vlm.logger import LogManager
from beer_vlm.language_model import AbstractLanguageModel
class AbstractPrompter(abc.ABC):
    def __init__(self, lm: AbstractLanguageModel, system_prompt: str="You are helpful assistant", name="abstract"):
        self.name = name
        self.lm = lm
        self.system_prompt = system_prompt
        
    @abc.abstractmethod
    def require_prompters(self) ->set[str]:
        pass
        
    @abc.abstractmethod
    async def query(self, image: Optional[str], **results) -> str:
        pass