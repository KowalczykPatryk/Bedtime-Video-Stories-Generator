"""
This module contains TTSClient class that can be used for inference with the tortoise-tts model
"""

from logging import Logger
import logging
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
    def __init__(self, log: Logger, voice_clips_filepaths: list[str] = None, voice: str = None):
        self.logger = log
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
        self.tts = api.TextToSpeech(use_deepspeed=False, kv_cache=False, half=False)

    def generate(self, text: str, filepath: str):
        """
        Calls the model with the given text and saves it in the provided filepath
        Note file extension has to be .wav
        """
        self.logger.info("TTS Starting generation")
        with torch.no_grad():
            # Pulse Code Modulation is a method of digitising analog signals by sampling
            # the signal’s amplitude at regular intervals and then
            # encoding these samples into binary numbers.
            # Here audio is just numbers inside torch.Tensor
            pcm_audio = self.tts.tts_with_preset(
                text,
                voice_samples=self.reference_clips,
                preset="fast"
            )
        self.logger.info("TTS Generation ended")

        src = pcm_audio.squeeze(0).cpu()

        self.logger.info("TTS Saving file")

        # wav file format after some header saves raw PCM samples without any compression
        torchaudio.save(
            filepath,
            src,
            24000
        )
        self.logger.info("TTS Saved successfully")

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="file.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
    tts = TTSClient(logger, voice="train_dotrice")
    tts.generate("""
                 Once upon a time, there was a gentle adventurer named Elara who traveled far and wide, her only companions a sturdy walking stick and a small white teapot.
                """,
                "test1.wav"
            )
