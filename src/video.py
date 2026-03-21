"""
Contains all functions needed to combine video from the images and audio
"""

from moviepy import AudioFileClip, AudioClip, CompositeAudioClip,\
    ImageClip, TextClip, CompositeVideoClip
from moviepy import concatenate_videoclips, concatenate_audioclips
from moviepy.video.fx import FadeIn, FadeOut


def create_video(images_filepaths: list[str],
                 audio_filepaths: list[str],
                 paragraphs: list[str],
                 video_filepath: str,
                 background_music_filepath: str) -> None:
    """
    Constructs video from the images and audio files.
    Displays text on top of the video.
    """
    if len(images_filepaths) != len(audio_filepaths) != len(paragraphs):
        raise ValueError(
            "To generate image there must as many images as audio files"
            )

    video_clips = []
    for i, (image_filepath, audio_filepath, paragraph) in enumerate(zip(images_filepaths, audio_filepaths, paragraphs)):
        silence = AudioClip(lambda t: 0, duration=0.2, fps=44100)
        audio = AudioFileClip(audio_filepath)
        audio = concatenate_audioclips([audio, silence])
        if i == 0:
            silence = AudioClip(lambda t: 0, duration=1, fps=44100)
            audio = concatenate_audioclips([silence, audio])
        image = ImageClip(image_filepath)
        clip = image.with_duration(audio.duration)
        clip = clip.with_audio(audio)
        txt_clip = TextClip(
            text=paragraph,
            font_size = 30,
            bg_color = (255, 255, 255, 140),
            color=(0, 0, 0),
            size=(image.w - 120, None),
            method='caption',
            margin=(30, 30),
            transparent=True,
            text_align='center',
            vertical_align='center',
            interline=9,
            duration= audio.duration
            )
        txt_clip = txt_clip.with_position(((image.w - txt_clip.w)/2, image.h - txt_clip.h - 30))
        clip = CompositeVideoClip([clip, txt_clip])
        video_clips.append(clip)

    for i in range(len(video_clips) - 1):
        video_clips[i] = FadeOut(0.5).apply(video_clips[i])
        video_clips[i+1] = FadeIn(0.5).apply(video_clips[i+1])

    video = concatenate_videoclips(video_clips)
    video = FadeIn(0.5).apply(video)
    video = FadeOut(0.5).apply(video)

    background_music = AudioFileClip(
        background_music_filepath).with_duration(video.duration)

    audio_combined = CompositeAudioClip(
        [
            video.audio,
            background_music.with_volume_scaled(0.4)
        ]
    )
    video = video.with_audio(audio_combined)

    video.write_videofile(video_filepath, fps=24)


if __name__ == "__main__":
    create_video(
        ["test/images/example_image.jpg", "test/images/example_image.jpg"],
        ["test/audio/example_audio.wav", "test/audio/example_audio.wav"],
        [
            "This is the text of the paragraph 0. It contains bedtime story for kids. This sentence is additional because each paragraph is quite long. This is the text of the paragraph 0. It contains bedtime story for kids. This sentence is additional because each paragraph is quite long.",
            "This is the text of the paragraph 1. It contains bedtime story for kids. This sentence is additional because each paragraph is quite long. This is the text of the paragraph 0. It contains bedtime story for kids. This sentence is additional because each paragraph is quite long."
        ],
        "test/video/example.mp4", "music/background_music.mp3")
