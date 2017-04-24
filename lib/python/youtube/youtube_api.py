from json import loads

from requests import get

from lib.python.helpers import internet_on
from lib.python.youtube.youtube_datastructures import YoutubePlaylist, YoutubeVideo

YOUTUBE_API_PLAYLIST_URI = 'https://www.googleapis.com/youtube/v3/{}'


class YoutubePlaylistAPI:
    type = 'playlistItems'

    def __init__(self, api_key, playlist):
        self.api_key = api_key
        self.playlist = playlist
        self.next_page_token = None
        self.prev_page_token = None

    def get_youtube_playlist_items(self):
        if internet_on():
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
                YoutubeVideo(video['snippet']['resourceId']['videoId'], video['snippet']['title']))


class YoutubePlaylistsAPI:
    type = 'playlists'

    def __init__(self, channel_id, api_key):
        self.channel_id = channel_id
        self.api_key = api_key

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


# 'UCFyI2wXdWdlgekzUXKp6ErQ',
if __name__ == '__main__':
    playlists = YoutubePlaylistsAPI('UCFyI2wXdWdlgekzUXKp6ErQ',
                                    'AIzaSyBWpeVHM7GHqBA-TVeajyJdliZNXflDEHI').get_all_playlists()
    for playlist in playlists:
        print(playlist)
        # playlist = YoutubePlaylist('PLCt9IUNM0_axDIeyhOwstQiAe3o8sTKHz', 'Deep')
        y = YoutubePlaylistAPI('AIzaSyBWpeVHM7GHqBA-TVeajyJdliZNXflDEHI', playlist)
        y.get_youtube_playlist_items()

        for video in y.playlist:
            print(video)
