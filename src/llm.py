"""
Using the OpenAI SDK to connect to OpenRouter
"""

import random
from logging import Logger
from openai import OpenAI
from src.utils import get_paragraphs

class LLMClient:
    """Sends prompt to the OpenRouter and retreives the response"""
    def __init__(self, model: str, api_key: str,
                 base_url: str = "https://openrouter.ai/api/v1", logger: Logger=None):
        self.llm_client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.logger = logger

    def ask(self, user: str, system: str = None, **kwargs):
        """Calls OpenRouter API"""
        assert user.strip() != "", "Prompt is empty."
        messages = [{"role": "user", "content": user}]
        if system:
            messages.insert(0, {"role": "system", "content": system})
        res = self.llm_client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        ).choices[0].message.content
        return res

    def generate_story(self,
                       story_user_prompt_filepath: str,
                       story_system_prompt_filepath: str,
                       seed_words_filepaths: list[str]) -> str | list[str]:
        """
        Generates story based on the seed words and optionally returns list of paragraphs

        story_user_prompt - the path to the file in which prompt for the llm is located
        story_system_prompt - the path to the file in which system prompt is located
        seed_words_filepaths - 
        """
        seed_words = []
        for filepath in seed_words_filepaths:
            with open(filepath, encoding="utf-8") as f:
                seed_words.append(random.choice(f.readlines()).strip())
        with open(story_user_prompt_filepath, encoding="utf-8") as story_user_prompt_file, \
            open(story_system_prompt_filepath, encoding="utf-8") as story_system_prompt_file:
            user_prompt = story_user_prompt_file.read().format(
                seed_words= ", ".join(seed_words)
            )
            res = self.ask(
                user=user_prompt, system=story_system_prompt_file.read()
            )

        if self.logger:
            self.logger.info("Seed words are: %s", ", ".join(seed_words))
            self.logger.info("The story:")
            self.logger.info(res)

        return res

    def generate_paragraphs_image_descriptions(self,
                                               description_for_image_prompt_filepath: str,
                                               story: str,
                                               para_sep: str = "\n\n") -> list[str]:
        """Returns list of the descriptions for each paragraph"""
        with open(description_for_image_prompt_filepath, encoding="utf-8") as dfip_file:
            template = dfip_file.read()

        paragraphs_descriptions = []

        for i, paragraph in enumerate(get_paragraphs(story, para_sep)):
            if not paragraph.strip():
                continue
            desc = template.format(paragraph=paragraph, whole_story=story)
            paragraphs_descriptions.insert(
                i,
                self.ask(user=desc)
            )
            if self.logger:
                self.logger.info("Paragraph: %s", paragraph)
                self.logger.info("Description: %s", paragraphs_descriptions[i])
        return paragraphs_descriptions

    def ask_from_file(self, filepath: str) -> str:
        """Prompt is taken from the provided file"""
        with open(filepath, encoding="utf-8") as file:
            return self.ask(file.read())
