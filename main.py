"""
This module runs the whole process
"""

import os
import random
import logging
from dotenv import load_dotenv
from src.llm_client import LLMClient
logger = logging.getLogger(__name__)


if __name__=="__main__":
    logging.basicConfig(filename="file.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
    load_dotenv()

    OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']
    assert OPENROUTER_API_KEY != "", \
    "You must set your OpenRouter API key in .env before running this"

    MODEL_NAME = "stepfun/step-3.5-flash:free"
    llm = LLMClient(model=MODEL_NAME, api_key=OPENROUTER_API_KEY)

    with open("prompts/story_user_prompt.txt", encoding="utf-8") as story_user_prompt_file, \
         open("prompts/story_system_prompt.txt", encoding="utf-8") as story_system_prompt_file, \
         open("seed_words/people.txt", encoding="utf-8") as people_file, \
         open("seed_words/animals.txt", encoding="utf-8") as animals_file, \
         open("seed_words/items.txt", encoding="utf-8") as items_file:
        person = random.choice(people_file.readlines()).strip()
        animal = random.choice(animals_file.readlines()).strip()
        item = random.choice(items_file.readlines()).strip()
        user_prompt = story_user_prompt_file.read().format(
            seed_words=f"{person}, {animal} and {item}"
        )
        res = llm.ask(
            user=user_prompt, system=story_system_prompt_file.read()
        ).choices[0].message.content

    logger.info("Seed words are: %s, %s and %s", person, animal, item)
    logger.info("The story:")
    logger.info(res)
    paragraphs = res.split("\n\n")
    for paragraph in paragraphs:
        logger.info("start %s stop\n", paragraph)

    with open("prompts/description_for_image_prompt.txt", encoding="utf-8") as dfip_file:
        template = dfip_file.read()

    paragraphs_descriptions = {}
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        desc = template.format(paragraph=paragraph, whole_story=res)
        paragraphs_descriptions[paragraph] = llm.ask(
            user=desc
        ).choices[0].message.content
        logger.info("Description: %s", paragraphs_descriptions[paragraph])
