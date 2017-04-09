class YoutubeVideo:
    def __init__(self, video_id, title):
        self.video_id = video_id
        self.title = title


class YoutubePlaylist:
    def __init__(self, etag, id, channel_id, api_key, playlist_id, title):
        self.etag = etag
        self.id = id
        self.channel_id = channel_id
        self.api_key = api_key
        self.playlist_id = playlist_id
        self.title = title

    def get_playlist_items(self):
        # TODO
        pass
