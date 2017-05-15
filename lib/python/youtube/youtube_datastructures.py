import sys
from os.path import realpath, join, dirname

import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

CLIENT_SECRETS_FILE = join(dirname(realpath(__file__)), '..\..\..\client_secret.json')

YOUTUBE_READ_WRITE_SSL_SCOPE = 'https://www.googleapis.com/auth/youtubepartner ' \
                               'https://www.googleapis.com/auth/youtube ' \
                               'https://www.googleapis.com/auth/youtube.force-ssl'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
MISSING_CLIENT_SECRETS_MESSAGE = 'WARNING: Please configure OAuth 2.0'


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage('%s-oauth2.json' % sys.argv[0])
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
    return build(API_SERVICE_NAME, API_VERSION, http=credentials.authorize(httplib2.Http()))


service = get_authenticated_service()


class YoutubeVideo:
    YOUTUBE_URI = 'https://youtu.be/'

    def __init__(self, url_id, title, video_id):
        self.url_id = url_id
        self.title = title
        self.video_id = video_id

    def __str__(self):
        return '{} ( {} ) '.format(self.title.encode('utf-8'), self.get_full_url())

    def get_full_url(self):
        return '{}{}'.format(YoutubeVideo.YOUTUBE_URI, self.url_id)


class YoutubePlaylist:
    def __init__(self, playlist_id, title, number_of_videos, auto_remove_video=False):
        self.playlist_id = playlist_id
        self.title = title
        self.number_of_videos = number_of_videos
        self.videos = []
        self._current_video = 0
        self.auto_remove_video = auto_remove_video

    def __str__(self):
        return '{} ({}) - {}'.format(self.title, self.number_of_videos, self.playlist_id)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_video >= len(self.videos):
            raise StopIteration
        else:
            self._current_video += 1
            return self.videos[self._current_video - 1]

    def __len__(self):
        return len(self.videos)

    def remove_video(self, video):
        service.playlistItems().delete(id=video.video_id).execute()
