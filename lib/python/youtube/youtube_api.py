from json import loads

from requests import get

from lib.python.helpers import check_internet
from lib.python.youtube.youtube_datastructures import YoutubePlaylist, YoutubeVideo

YOUTUBE_API_PLAYLIST_URI = 'https://www.googleapis.com/youtube/v3/{}'


class YoutubePlaylistAPI:
    type = 'playlistItems'

    def __init__(self, api_key, playlist, logger):
        self.api_key = api_key
        self.playlist = playlist
        self.next_page_token = None
        self.prev_page_token = None
        self.logger = logger

    def get_youtube_playlist_items(self):
        if check_internet(self.logger):
            while True:
                if not self.next_page(max_results=50):
                    break

    def next_page(self, max_results=5):
        params = {'part': 'snippet', 'maxResults': max_results, 'playlistId': self.playlist.playlist_id,
                  'key': self.api_key}
        is_next_page = False
        if not self.next_page_token and not self.prev_page_token:
            params['pageToken'] = ''
        elif self.next_page_token:
            params['pageToken'] = self.next_page_token

        data = current_page_items(YoutubePlaylistAPI.type, params)
        self.parse_videos(data)

        if 'nextPageToken' in data:
            self.next_page_token = data['nextPageToken']
            is_next_page = True
        if 'prevPageToken' in data:
            self.prev_page_token = data['prevPageToken']
        return is_next_page

    def parse_videos(self, data):
        for video in data['items']:
            self.playlist.videos.append(
                YoutubeVideo(video['snippet']['resourceId']['videoId'], video['snippet']['title'], video['id']))


class YoutubePlaylistsAPI:
    type = 'playlists'

    def __init__(self, channel_id, api_key, logger):
        self.channel_id = channel_id
        self.api_key = api_key
        self.logger = logger

    def get_all_playlists(self):
        params = {'part': 'snippet,contentDetails', 'channelId': self.channel_id, 'key': self.api_key}
        data = current_page_items(YoutubePlaylistsAPI.type, params)
        return self.parse_playlists(data)

    def parse_playlists(self, data):
        playlists = []
        for playlist in data['items']:
            playlists.append(
                YoutubePlaylist(playlist['id'], playlist['snippet']['title'], playlist['contentDetails']['itemCount']))
        return playlists


def current_page_items(type, params):
    result = get(YOUTUBE_API_PLAYLIST_URI.format(type), params=params)
    data = loads(result.text)
    return data
