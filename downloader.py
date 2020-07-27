from pytube import YouTube
import os
import sys

video_size = 1
times_prompted_video_url = 0
times_prompted_download_mode = 0

def print_welcome_message():
    print('\n\n**** Welcome to the YouTube video downloader ****\n\n')

def invalid_input_exit():
    print('Please re-run this program when you have some valid input.')
    print('Exiting ...')
    sys.exit(1)

# prompts the user a maximum of 3 times and does basic verification on input, further verification is done in verify_video_existence.
def prompt_video_url():
    global times_prompted_video_url
    times_prompted_video_url += 1
    if times_prompted_video_url > 3:
        invalid_input_exit()
    user_input_valid = False
    if not user_input_valid:
        user_input = input('\nPlease give me the URL of your video: ')
        user_input_valid = True if user_input.startswith('https://www.youtube.com/watch?v=') else prompt_video_url()
    return user_input

def prompt_download_mode():
    global times_prompted_download_mode
    times_prompted_download_mode += 1
    if times_prompted_download_mode > 3:
        invalid_input_exit()
    user_input = input('\nPlease Enter a download mode: \n0: Video only\n1: Audio only\n2: Both video and audio\n\n')
    acceptable_user_inputs = ['0', '1', '2']
    if user_input not in acceptable_user_inputs:
        print('Unacceptable input, please enter 0, 1, or 2')
        prompt_download_mode()
    return user_input


# Verifies video loaded correctly before proceeding
def verify_video_existence(video_url):
    try:
        return YouTube(video_url)
    except Exception as e:
        print(e)
        print('There was a problem loading the video, please double check the URL')
        print('Exiting ...')
        sys.exit(1)

# callback function used to show progress for video download
def show_progress(chunk, file_handler, bytes_remaining):
    global video_size
    print(round((1-bytes_remaining/video_size)*100, 2), '% done...')

# Downloads a video at the highest resolution possible given the video object
def download_video(video):
    global video_size
    video.register_on_progress_callback(show_progress)
    highest_res_stream = video.streams.get_highest_resolution()
    video_size = highest_res_stream.filesize
    print('Downloading ...')
    print('File saved to ' + highest_res_stream.download(filename_prefix='video-'))
    print('Downloaded "' + video.title + '" by ' + video.author)
    #os.remove(video.title + '.mp4')

def download_audio(video):
    global video_size
    video.register_on_progress_callback(show_progress)
    audio_stream = video.streams.get_audio_only()
    video_size = audio_stream.filesize
    print('Downloading ...')
    print('File saved to ' + audio_stream.download(filename_prefix='audio-'))
    print('Downloaded "' + video.title + '" by ' + video.author + ' as audio file')


def download(download_mode, youtube_obj):
    if download_mode == 0:
        download_video(youtube_obj)
    elif download_mode == 1:
        download_audio(youtube_obj)
    else:
        download_video(youtube_obj)
        download_audio(youtube_obj)


def main():
    print_welcome_message()
    video_url = prompt_video_url()
    youtube_obj = verify_video_existence(video_url)
    download_mode = int(prompt_download_mode())
    download(download_mode, youtube_obj)

main()
