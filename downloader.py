from pytube import YouTube
import os

video_size = 1

def show_progress(chunk, file_handler, bytes_remaining):
    global video_size
    print(round((1-bytes_remaining/video_size)*100, 2), '% done...')


def download_video(video_url):
    global video_size
    video = YouTube(video_url)
    video.register_on_progress_callback(show_progress)
    highest_res_stream = video.streams.get_highest_resolution()
    video_size = highest_res_stream.filesize
    print('Downloading ...')
    highest_res_stream.download()
    print('Downloaded "' + video.title + '" by ' + video.author)
    os.remove(video.title + '.mp4')

download_video('https://www.youtube.com/watch?v=668nUCeBHyY')
