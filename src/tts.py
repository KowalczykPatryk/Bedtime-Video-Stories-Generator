"""
This module contains TTSClient class that can be used for inference with the tts models
"""

from boson_multimodal.serve.serve_engine import HiggsAudioServeEngine, HiggsAudioResponse
from boson_multimodal.data_types import ChatMLSample, Message, AudioContent

import torch
import torchaudio


class TTSClient:
    """
    Manages interactions with the text-to-speech models from bosonai
    """
    def __init__(self, model_path: str = "bosonai/higgs-audio-v2-generation-3B-base",
                 audio_tokenizer_path: str = "bosonai/higgs-audio-v2-tokenizer"):
        self.model_path = model_path
        self.audio_tokenizer_path = audio_tokenizer_path

    def generate(
            self,
            text: str,
            result_filepath: str,
            system_prompt: str
            ):
        """
        Passes the text for which speech will be generated with the system prompt
        which tunes features and quality of the voice.
        """
        messages = [
            Message(
                role="system",
                content=system_prompt,
            ),
            Message(
                role="user",
                content=text,
            ),
        ]
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(device)
        serve_engine = HiggsAudioServeEngine(
            self.model_path,
            self.audio_tokenizer_path,
            device=device
            )
        output: HiggsAudioResponse = serve_engine.generate(
            chat_ml_sample=ChatMLSample(messages=messages),
            max_new_tokens=1024,
            temperature=0.3,
            top_p=0.95,
            top_k=50,
            stop_strings=["<|end_of_text|>", "<|eot_id|>"],
        )
        torchaudio.save(
            result_filepath,
            torch.from_numpy(output.audio)[None, :],
            output.sampling_rate
            )



if __name__ == "__main__":
    tts = TTSClient()
    with open("prompts/tts_system_prompt.txt", encoding="utf-8") as f1,\
    open("prompts/tests/tts_user_prompt.txt", encoding="utf-8") as f2:
        tts.generate(
            f2.read(),
            "test3.wav",
            f1.read()
            )
