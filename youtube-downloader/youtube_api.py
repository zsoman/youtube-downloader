from requests import get

# from .helpers import internet_on

YOUTUBE_API_PLAYLIST_URI = 'https://www.googleapis.com/youtube/v3/playlistItems'


class YoutubePlaylistAPI:
    def __init__(self, api_key, channel_id, playlist_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.playlist_id = playlist_id
        self.next_page_token = None
        self.previous_page_token = None

    def get_youtube_playlist_items(self):
        if internet_on():
            # TODO
            pass

    def next_page(self, max_results=5):
        params = {'part': 'snippet', 'maxResults': max_results, 'playlistId': self.playlist_id, 'key': self.api_key}
        if not self.next_page_token and not self.previous_page_token:
            params['pageToken'] = ''
        elif self.next_page_token:
            params['pageToken'] = self.next_page_token
        self.current_page_items(params)

    def current_page_items(self, params):
        result = get(YOUTUBE_API_PLAYLIST_URI, params=params)
        print(result.url)
        print(result.text)


if __name__ == '__main__':
    y = YoutubePlaylistAPI('AIzaSyBWpeVHM7GHqBA-TVeajyJdliZNXflDEHI', 'UCFyI2wXdWdlgekzUXKp6ErQ',
                           'PLCt9IUNM0_axDIeyhOwstQiAe3o8sTKHz')
    y.next_page()
