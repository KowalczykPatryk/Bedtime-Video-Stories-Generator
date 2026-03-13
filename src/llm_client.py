"""
Using the OpenAI SDK to connect to OpenRouter
"""

from openai import OpenAI

class LLMClient:
    """Sends prompt to the OpenRouter and retreives the response"""
    def __init__(self, model: str, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.llm_client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

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
        )
        return res
