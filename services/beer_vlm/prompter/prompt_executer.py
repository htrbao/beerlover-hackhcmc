from typing import Any, List, Optional
from .abstract_prompter import AbstractPrompter
import time


class PromptExecutor(object):
    
    def __init__(self) -> str:
        self.prompters = []
        
    
    def add_prompter(self, prompter: AbstractPrompter):
        self.prompters.append(prompter)
        return self
        
    def build(self):
        check_list = set()
        assert len(self.prompters), "length of prompters should be greater than 0"
        
        # assert self.prompters[-1].name == "final", "Final prompter always at the end of the list"
        for prompter in self.prompters:
            assert prompter.require_prompters().issubset(check_list), f"{prompter.name} prompter do not meet the requirements"
            check_list.add(prompter.name)
        return self
    async def execute(self, image: str, results: Optional[dict] = None) -> dict:
        """
        :param image: base64 encoded image
        :type: str
        """
        if results is None:
            results = dict()
        for prompter in self.prompters:
            results[prompter.name] = await prompter.query(image, **results)
        
        return results
        