from pytube import YouTube
import os
import sys

video_size = 1
times_prompted = 0

def print_welcome_message():
    print('**** Welcome to the YouTube video downloader ****\n\n')

# prompts the user a maximum of 3 times and does basic verification on input, further verification is done in verify_video_existence.
def prompt_video_url():
    global times_prompted
    times_prompted += 1
    if times_prompted > 3:
        print('Please re-run this program when you have some valid input.')
        print('Exiting ...')
        sys.exit(1)
    user_input_valid = False
    while not user_input_valid:
        user_input = input('Please give me the URL of your video: ')
        user_input_valid = True if user_input.startswith('https://www.youtube.com/watch?v=') else prompt_video_url()
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
    print('File saved to ' + highest_res_stream.download())
    print('Downloaded "' + video.title + '" by ' + video.author)
    os.remove(video.title + '.mp4')

print_welcome_message()
download_video(verify_video_existence(prompt_video_url()))
