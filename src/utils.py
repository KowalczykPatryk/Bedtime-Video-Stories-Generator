"""
Utility functions
"""
import os
from pydub import AudioSegment

def get_paragraphs(story: str, split_str: str = "\n\n") -> list[str]:
    """Returns list of the paragraphs by spliting on the desired split_str"""
    return story.split(split_str)

def delete_files(filepaths: list[str]):
    """Removes files"""
    for filepath in filepaths:
        if os.path.isfile(filepath):
            os.remove(filepath)

def concatenate_audio(filepaths: list[str], filepath: str):
    """Concatenes .wav files into one and saves it in the provided filepath"""
    combined = AudioSegment.empty()

    for f in filepaths:
        combined += AudioSegment.from_wav(f)

    combined.export(filepath, format="wav")
