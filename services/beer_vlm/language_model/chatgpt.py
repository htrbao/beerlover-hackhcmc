# Copyright (c) 2023 ETH Zurich.
#                    All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# main author: Nils Blach

import backoff
import openai
import logging
import os
import random
import time
import requests
import asyncio
from openai import AsyncOpenAI
from typing import List, Dict, Union, Optional

from .abstract_language_model import AbstractLanguageModel
from services.beer_vlm.configs import OPENAI_API_KEY, ORGANIZATION_KEY
from services.beer_vlm.logger import LogManager


class ChatGPT(AbstractLanguageModel):
    """
    The ChatGPT class handles interactions with the OpenAI models using the provided configuration.

    Inherits from the AbstractLanguageModel and implements its abstract methods.
    """

    def __init__(
        self,
        model_name: str = "gpt-4o",
        log_mng: Optional[LogManager] = None,
        system_prompt="You are helpful assistant.",
        cache: bool = False,
    ) -> None:
        """
        Initialize the ChatGPT instance with configuration, model details, and caching options.

        :param config_path: Path to the configuration file. Defaults to "".
        :type config_path: str
        :param model_name: Name of the model, default is 'chatgpt'. Used to select the correct configuration.
        :type model_name: str
        :param cache: Flag to determine whether to cache responses. Defaults to False.
        :type cache: bool
        """
        super().__init__(model_name, cache)
        self.config: Dict = self.config[model_name]
        # The model_id is the id of the model that is used for chatgpt, i.e. gpt-4, gpt-3.5-turbo, etc.
        self.model_id: str = self.config["model_id"]
        # The prompt_token_cost and response_token_cost are the costs for 1000 prompt tokens and 1000 response tokens respectively.
        self.prompt_token_cost: float = self.config["prompt_token_cost"]
        self.response_token_cost: float = self.config["response_token_cost"]
        # The temperature of a model is defined as the randomness of the model's output.
        self.temperature: float = self.config["temperature"]
        # The maximum number of tokens to generate in the chat completion.
        self.max_tokens: int = self.config["max_tokens"]
        # The stop sequence is a sequence of tokens that the model will stop generating at (it will not generate the stop sequence).
        # The account organization is the organization that is used for chatgpt.
        self.organization: str = ORGANIZATION_KEY
        # The api key is the api key that is used for chatgpt. Env variable OPENAI_API_KEY takes precedence over config.
        self.api_key: str = OPENAI_API_KEY
        if self.api_key == "":
            raise ValueError("OPENAI_API_KEY is not set")
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY, organization=ORGANIZATION_KEY)
        self.log_mng = log_mng

    async def query(
        self,
        query: str,
        image: Optional[str],
        num_responses: int = 1,
        system_prompt: str = "You are helpful assistant.",
        main_image: Optional[str] = None,
    ) -> Dict:
        """
        Query the OpenAI model for responses.

        :param query: The query to be posed to the language model.
        :type query: str
        :param image: The base64 encoded image
        :type image: str
        :param num_responses: Number of desired responses, default is 1.
        :type num_responses: int
        :return: Response(s) from the OpenAI model.
        :rtype: Dict
        """
        start_time = time.monotonic()
        json_format = None
        if "JSON" in query:
            json_format = {"type": "json_object"}
        message = [{"role": "system", "content": system_prompt}]

        user_message = {"role": "user"}

        if image is not None:
            user_message["content"] = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image,#f"data:image/jpeg;base64,{image}",
                        "detail": "high"
                        }
                    
                },
                {"type": "text", "text": query},
            ]
            if main_image is not None:
                user_message["content"] = [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image,#f"data:image/jpeg;base64,{main_image}",
                            "detail": "high"
                            }
                        
                    },
                    {"type": "text", "text": "This is the overall image of below image. You should use this to increase the accurate of your answer"}
                ] + user_message.get("content", [""])
        else:
            user_message["content"] = {"role": "user", "content": query}

        message.append(user_message)
        # print(message)
        if self.cache and query in self.respone_cache:
            return self.respone_cache[query]

        if num_responses == 1:
            response = await self.chat(message, num_responses, json_format)
        else:
            response = []
            next_try = num_responses
            total_num_attempts = num_responses
            while num_responses > 0 and total_num_attempts > 0:
                try:
                    assert next_try > 0
                    res = await self.chat(message, next_try, json_format)
                    response.append(res)
                    num_responses -= next_try
                    next_try = min(num_responses, next_try)
                except Exception as e:
                    next_try = (next_try + 1) // 2
                    await asyncio.sleep(random.randint(1, 3))
                    total_num_attempts -= 1

        if self.cache:
            self.respone_cache[query] = response
        print("time: ", time.monotonic()- start_time)
        return response

    @backoff.on_exception(backoff.expo, openai.OpenAIError, max_time=10, max_tries=6)
    async def chat(
        self, messages: List[Dict], num_responses: int = 1, json_format=None
    ) -> Dict:
        """
        Send chat messages to the OpenAI model and retrieves the model's response.
        Implements backoff on OpenAI error.

        :param messages: A list of message dictionaries for the chat.
        :type messages: List[Dict]
        :param num_responses: Number of desired responses, default is 1.
        :type num_responses: int
        :return: The OpenAI model's response.
        :rtype: Dict
        """
        response = await self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            n=num_responses,
            response_format=json_format,
        )
        self.prompt_tokens += response.usage.prompt_tokens
        self.completion_tokens += response.usage.completion_tokens
        prompt_tokens_k = float(self.prompt_tokens) / 1000.0
        completion_tokens_k = float(self.completion_tokens) / 1000.0
        self.cost = (
            self.prompt_token_cost * prompt_tokens_k
            + self.response_token_cost * completion_tokens_k
        )
        return response

    async def get_response_texts(self, query_response: Union[List[Dict], Dict]) -> List[str]:
        """
        Extract the response texts from the query response.

        :param query_response: The response dictionary (or list of dictionaries) from the OpenAI model.
        :type query_response: Union[List[Dict], Dict]
        :return: List of response strings.
        :rtype: List[str]
        """
        if isinstance(query_response, Dict) or (
            isinstance(query_response, object) and not isinstance(query_response, list)
        ):
            query_response = [query_response]

        return [
            choice.message.content
            for response in query_response
            for choice in response.choices
        ]
