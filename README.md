# Bedtime Stories

Program works in two modes:
- user provides keywords which will work as he seed for the LLM to generate narative of the story
- keywords are randomly selected from the predefined set of the topics  

Project is written fully in python. Important part is carefully prepared prompts for LLM and generative model that are placed in separate files. The aim is to experiment and explore already trained models. For LLM one idea is to use free models that are available on [openrouter](https://openrouter.ai/). The other is to download open source pretrained model and fine-tune it and optimize for the children stories generation so that it could be run locally with relatively slow NVIDIA GPU or optionally CPU if possible because CPU fallback really slows down generation.

The LLM given the seed words generates plot of the story and separates paragraphs by `\n\n` so that later each one can be taken invidually. Each paragraphs is provided to the LLM to generate descriptive prompt for the image-generate model. Also each one the same paragraphs is inputed to the TTS model to generate voice over for the story. Based on the length of audio files images are seamed into one video. The text of the paragraph is placed above the image while being played.

Additional layer is to create automation pipeline for the whole process where when provided necessary authentications, the generation can be scheduled for the selected date and time. Then uploaded directly to the youtube channel.

To improve output quality of the text-to-image model I used information from this [paper](https://arxiv.org/pdf/2209.11711) and this [website](https://getimg.ai/guides/guide-to-writing-text-to-image-prompts). Negative prompts can improve quality, more about this [here](https://medium.com/@johnnythedeveloper/negative-prompts-for-perfect-ai-image-generation-4b45744363c7). Text-to-image api: [deapi](https://docs.deapi.ai/)

As the text-to-speech model at the beggining I used [Tortoise-TTS](https://github.com/neonbjb/tortoise-tts). [Here](https://medium.com/@martin-thissen/tortoise-tts-fully-explained-part-1-architecture-design-ec4047c5ab75) is good explanation of the architecture used in it. However on the whole paragraph the process run out of the available memory so model was used for each sentence separatelly, but for longer sentences still it wasn't enought. Then I switched to smaller models from [coqui-ai](https://github.com/coqui-ai/TTS) which were fast but the quality was not sufficient. Then I found [Higgs-Audio](https://github.com/boson-ai/higgs-audio).

Model weights must be loaded to the RAM for the inference. [Swap space](https://www.geeksforgeeks.org/operating-systems/swap-space-in-operating-system/) helped with OS killing python process for requesting too much RAM.

Creating swap space:  
   ```bash
   sudo fallocate -l [SIZE]G /[FILENAME]
   sudo chmod 600 /[FILENAME]
   sudo mkswap /[FILENAME]
   sudo swapon /[FILENAME]
   free -h
   ```

For working with video I used [MoviePy](https://zulko.github.io/moviepy/getting_started/index.html#getting-started). Here is introduction [intro](https://www.geeksforgeeks.org/python/introduction-to-moviepy/).

As the background music I used [this](https://soundcloud.com/rossbugden/bedtime-stories).

## Notes

Repo cloning:  
   ```bash
   git clone https://github.com/KowalczykPatryk/lullabby_stories.git
   cd lullabby_stories
   ```

Create and activate a virtual environment:  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

Save currently installed dependencies:

   ```bash
   pip freeze > requirements.txt
   ```

Hugging Face token and all the other can be stored in the `.env` file in the project root:

   ```bash
   # .env
   HUGGINGFACE_TOKEN=hf_xxxYourTokenxxx
   ```


