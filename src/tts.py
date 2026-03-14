"""
This module contains TTSClient class that can be used for inference with the tortoise-tts model
"""

import torch
import torchaudio

from tortoise import api
from tortoise.utils.audio import load_audio, load_voice


class TTSClient:
    """
    This class uses tortoise-tts api to generate audio file for the given text
    voice_clips_filepaths - filepaths to the custom samples of some voice
    that will be used to clone the voice in them
    voice - string that coresponds to the name of the voice saved inside tortoise-tts package
    """
    def __init__(self, voice_clips_filepaths: list[str] = None, voice: str = None):
        if voice_clips_filepaths and voice:
            raise ValueError("Specify either voice clips or built-in voice, not both")
        if voice_clips_filepaths:
            # sampling rate is in Hz and means how many times in a second
            # measurement was taken because audio in files is not saved continuously
            # but in discrete form
            self.reference_clips = [load_audio(p, 22050) for p in voice_clips_filepaths]
        if voice:
            voice_samples, _ = load_voice(voice)
            self.reference_clips = voice_samples
        self.tts = api.TextToSpeech(use_deepspeed=True, kv_cache=True, half=True)

    def generate(self, text: str, filepath: str):
        """
        Calls the model with the given text and saves it in the provided filepath
        Note file extension has to be .wav
        """

        with torch.no_grad():
            # Pulse Code Modulation is a method of digitising analog signals by sampling
            # the signal’s amplitude at regular intervals and then
            # encoding these samples into binary numbers.
            # Here audio is just numbers inside torch.Tensor
            pcm_audio = self.tts.tts_with_preset(
                text,
                voice_samples=self.reference_clips,
                preset="standard"
            )

        # wav file format after some header saves raw PCM samples without any compression
        torchaudio.save(
            filepath,
            pcm_audio.squeeze(0).cpu(),
            24000
        )

if __name__ == "__main__":
    tts = TTSClient(voice="train_dotrice")
    tts.generate("""
                 Tomas picked up the crown, and as soon as it touched his hands, a warm feeling spread through him. A tiny voice, like the rustle of leaves, whispered: "This crown is enchanted. It will grant one wish to whoever wears it, but only if the wish comes from a selfless heart." Tomas thought of his village, which had been suffering from a long drought. Without hesitation, he placed the crown on his head and wished for rain to water the parched fields and bring life back to the soil. Instantly, dark clouds gathered, and a gentle rain fell, soaking the earth and filling the villagers with joy.
                """,
                "test.wav"
            )
