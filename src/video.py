"""
Contains all functions needed to combine video from the images and audio
"""

from moviepy import AudioFileClip, AudioClip, CompositeAudioClip, concatenate_videoclips, concatenate_audioclips
from moviepy.video.VideoClip import ImageClip
from moviepy.video.fx import FadeIn, FadeOut

def create_video(images_filepaths: list[str],
                 audio_filepaths: list[str],
                 video_filepath: str,
                 background_music_filepath: str) -> None:
    """
    Constructs video from the images and audio files
    """
    if len(images_filepaths) != len(audio_filepaths):
        raise ValueError("To generate image there must as many images as audio files")

    video_clips = []
    for i, (image_filepath, audio_filepath) in enumerate(zip(images_filepaths, audio_filepaths)):
        silence = AudioClip(lambda t: 0, duration=0.2, fps=44100)
        audio = AudioFileClip(audio_filepath)
        audio = concatenate_audioclips([audio, silence])
        if i == 0:
            silence = AudioClip(lambda t: 0, duration=1, fps=44100)
            audio = concatenate_audioclips([silence, audio])
        image = ImageClip(image_filepath)
        clip = image.with_duration(audio.duration)
        clip = clip.with_audio(audio)
        video_clips.append(clip)

    for i in range(len(video_clips) - 1):
        video_clips[i] = FadeOut(0.5).apply(video_clips[i])
        video_clips[i+1] = FadeIn(0.5).apply(video_clips[i+1])

    video = concatenate_videoclips(video_clips)
    video = FadeIn(0.5).apply(video)
    video = FadeOut(0.5).apply(video)

    background_music = AudioFileClip(background_music_filepath).with_duration(video.duration)

    audio_combined = CompositeAudioClip(
        [
            video.audio,
            background_music.with_volume_scaled(0.3)
        ]
    )
    video = video.with_audio(audio_combined)

    video.write_videofile(video_filepath, fps=24)

# # Generate a text clip
# txt_clip = TextClip("GeeksforGeeks", fontsize = 70, color = 'white')

# # setting position of text in the center and duration will be 10 seconds
# txt_clip = txt_clip.set_pos('center').set_duration(10)

# # Overlay the text clip on the first video clip
# video = CompositeVideoClip([clip, txt_clip])

if __name__ == "__main__":
    create_video(
        ["test/images/test_image.jpeg", "test/images/test_image.jpeg"],
        ["test/audio/test_audio.mp3", "test/audio/test_audio.mp3"],
        "test/video/sth.mp4", "music/background_music.mp3")
    