import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from os.path import realpath, join, dirname

import youtube_dl
from tqdm import tqdm

from lib.python.file_handler import get_song_path, song_exists
from lib.python.youtube.youtube_api import YoutubePlaylistAPI, YoutubePlaylistsAPI

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Default logging level.
file_logger = RotatingFileHandler(join(dirname(realpath(__file__)), 'music-yt-dl.log'), maxBytes=5000000,
                                  backupCount=5)  # Main logging file.
file_logger.setLevel(logging.DEBUG)  # Main logging file's logging level.
console_logger = logging.StreamHandler()  # Console logging.
console_logger.setLevel(logging.INFO)  # Level of logging of STDout.
formatter = logging.Formatter('%(asctime)s - %(processName)s / %(threadName)s - %(name)s - %(levelname)s - %(message)s')
file_logger.setFormatter(formatter)
console_logger.setFormatter(formatter)
logger.addHandler(file_logger)
logger.addHandler(console_logger)


def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--chennel_id', type=str, help='The channel ID')
    parser.add_argument('-k', '--api_key', type=str, help='API key')
    parser.add_argument('-p', '--path', type=str, help='Base path to download the videos')
    parser.add_argument('-d', '--delete_video_playlist', nargs='*', type=str, default=[],
                        help='List of playlist names after download remove the videos from the playlist')
    parser.add_argument('-s', '--special_playlist', nargs='*', type=str, default=[],
                        help='List of playlist names which will be downloaded in "...\year\year season path"')
    args = parser.parse_args()

    playlists = get_playlists_to_download(args.chennel_id, args.api_key)
    for playlist in playlists:
        logger.info(playlist)
        playlist_videos = get_videos_to_download(playlist, args.api_key)

        for video in tqdm(playlist_videos):
            if not song_exists(video.title, playlist_videos.title, args.path, args.special_playlist):
                logger.debug('Started downloading {}'.format(video))
                attempt = 0
                while attempt < 5:
                    try:
                        download_video(video.get_full_url(),
                                       get_song_path(playlist_videos.title, args.path, args.special_playlist))
                    except Exception as ex:
                        logger.exception("Couldn't download {}".format(video))
                        attempt += 1
                    else:
                        if playlist_videos.title in args.delete_video_playlist:
                            playlist_videos.remove_video(video)
                            logging.debug('{} video is removed from {} playlist'.format(video, playlist_videos.title))
                        break
                if attempt == 5:
                    logger.error('Please download manually the {} video'.format(video))
            else:
                logging.debug('{} video already exists'.format(video))


def get_playlists_to_download(channel_id, api_key):
    return YoutubePlaylistsAPI(channel_id, api_key, logger).get_all_playlists()


def get_videos_to_download(playlist, api_key):
    y = YoutubePlaylistAPI(api_key, playlist, logger)
    y.get_youtube_playlist_items()
    return y.playlist


def my_hook(dl_dict):
    if dl_dict['status'] == 'finished':
        logger.debug('Done downloading, now converting {}'.format(dl_dict['filename'].replace('webm', 'mp3')))
    elif dl_dict['status'] == 'downloading':
        logger.debug('Started downloading {}'.format(dl_dict['filename'].replace('webm', 'mp3')))
    elif dl_dict['status'] == 'error':
        logger.error('An error occured: {}'.format(dl_dict))


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download_video(url, path):
    ydl_opts = {
        'writethumbnail': True,
        'format': 'bestaudio/best',
        'outtmpl': '{path}\%(title)s.%(ext)s'.format(path=path),
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
             'preferredcodec': 'mp3',
             'preferredquality': '192'},
            {'key': 'EmbedThumbnail'}],
        'logger': logger,
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    main()
