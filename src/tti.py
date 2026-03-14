"""
This module includes class for communication with the text-to-image model
"""

import time
from logging import Logger
import requests


class TTIClient:
    """
    Manages interactions with the text-to-image model api
    """
    def __init__(self, url: str, api_key: str, logger: Logger = None):
        self.url = url
        self.api_key = api_key
        self.logger = logger

    def generate_image(self, description: str,
                       output_image_filepath: str,
                       negative_prompt_words_filepaths: list[str] = None,
                       img_size: tuple[int] = (1920, 1080)):
        """
        description - prompt for the text-to-image model
        negative_prompt_words_filepaths - list of filepaths inside which 
        are words used in the negative prompt
        img_size - (width, height) of the output image
        """
        negative_prompts = []
        if negative_prompt_words_filepaths:
            for filepath in negative_prompt_words_filepaths:
                with open(filepath, encoding="utf-8") as f:
                    for word in f.readlines():
                        negative_prompts.append(word.strip())

        payload = {
            "prompt": description,
            "model": "Flux1schnell",
            "width": img_size[0],
            "height": img_size[1],
            "guidance": 7.5,
            "steps": 10,
            "seed": 42,
            "negative_prompt": ", ".join(negative_prompts) if negative_prompts else ""
        }
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.url, json=payload, headers=headers, timeout=10).json()

        url = f"https://api.deapi.ai/api/v1/client/request-status/{response['data']['request_id']}"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        while True:
            response = requests.get(url, headers=headers, timeout=10).json()
            if response["data"]["status"] in ("pending", "processing"):
                self.logger.info(response["data"]["progress"])
                time.sleep(20)
            elif response["data"]["status"] == "done":
                self.logger.info("Image generated")
                break
            elif response["data"]["status"] == "error":
                self.logger.info("Generation error")
                break

        if response["data"]["status"] == "done":
            response = requests.get(response["data"]["result_url"], timeout=10)
            print(response)
            with open(output_image_filepath, "wb") as f:
                f.write(response.content)
