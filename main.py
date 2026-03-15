"""
This module runs the whole process of video generation
"""

import os
import logging
from dotenv import load_dotenv
from src.llm import LLMClient
from src.utils import get_paragraphs, delete_files, concatenate_audio
from src.tti import TTIClient
from src.tts import TTSClient
from src.video import create_video


if __name__=="__main__":
    logger = logging.getLogger(__name__)
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

    story = llm.generate_story(
            "prompts/story_user_prompt.txt", 
            "prompts/story_system_prompt.txt", 
            ["seed_words/people.txt", "seed_words/animals.txt", "seed_words/items.txt"]
        )
    paragraphs = get_paragraphs(story)
    image_descriptions = llm.generate_paragraphs_image_descriptions(
            "prompts/description_for_image_prompt.txt",
            story
        )

    DEAPI_API_KEY = os.environ['DEAPI_API_KEY']

    URL = "https://api.deapi.ai/api/v1/client/txt2img"

    tti = TTIClient(URL, DEAPI_API_KEY)

    images_filepaths = []
    for i, description in enumerate(image_descriptions):
        FILEPATH = f"images/paragraph{i}.png"
        images_filepaths.append(FILEPATH)
        tti.generate_image(
            description,
            FILEPATH,
            [
                "negative_prompts/general.txt"
            ]
        )

    tts = TTSClient(logger, voice="train_dotrice")
    audio_paragraphs_filepaths = []
    for i, paragraph in enumerate(paragraphs):
        audio_sentences_filepaths = []
        for j, sentence in enumerate(list(map(lambda a: a.strip()+".", paragraph.split(".")[:-1]))):
            FILEPATH = f"audio/sentence{j}.wav"
            audio_sentences_filepaths.append(FILEPATH)
            tts.generate(sentence, FILEPATH)
        FILEPATH = f"audio/paragraph{i}.wav"
        audio_paragraphs_filepaths.append(FILEPATH)
        concatenate_audio(audio_sentences_filepaths, FILEPATH)
        delete_files(audio_sentences_filepaths)

    title = llm.ask_from_file("prompts/video_title_prompt.txt")

    VIDEO_FILEPATH = "video/"+"_".join(title.split(" ")) + ".mp4"

    create_video(images_filepaths, audio_paragraphs_filepaths, VIDEO_FILEPATH, "music/background_music.mp3")

    #delete_files(images_filepaths)
    #delete_files(audio_filepaths)
