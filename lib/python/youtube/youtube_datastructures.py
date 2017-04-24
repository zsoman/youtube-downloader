class YoutubeVideo:
    YOUTUBE_URI = 'https://youtu.be/'

    def __init__(self, video_id, title):
        self.video_id = video_id
        self.title = title

    def __str__(self):
        return '{} ( {}{} )'.format(self.title, YoutubeVideo.YOUTUBE_URI, self.video_id)


class YoutubePlaylist:
    def __init__(self, playlist_id, title, number_of_videos):
        self.playlist_id = playlist_id
        self.title = title
        self.number_of_videos = number_of_videos
        self.videos = []
        self._current_video = 0

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
