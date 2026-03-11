# Bedtime Stories

Program works in two modes:
- user provides keywords which will work as he seed for the LLM to generate narative of the story
- keywords are randomly selected from the predefined set of the topics  

Project is written fully in python. Important part is carefully prepared prompts for LLM and generative model that are placed in separate files. Aim is to experiment and explore already trained models. For LLM one idea is to use free models that are available on [openrouter](https://openrouter.ai/). The other is to download open source pretrained model and fine-tune it and optimize for the children stories generation so that it could be run locally with relatively slow NVIDIA GPU or optionally CPU if possible because CPU fallback really slows down generation. For image generation from description to explore is:
-  Stable Diffusion model

## Running Notes

Repo cloning:  
   ```bash
   git clone https://github.com/KowalczykPatryk/lullabby_stories.git
   cd lullabby_stories
```

Create and activate a virtual environment:  
    ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Hugging Face token:

   ```bash
   # .env
   HUGGINGFACE_TOKEN=hf_xxxYourTokenxxx
   ```

   **Important:** Do **not** commit `.env` to source control. It’s already in `.gitignore`.

---

