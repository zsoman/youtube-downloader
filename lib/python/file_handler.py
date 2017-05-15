from datetime import datetime
from functools import reduce
from os import makedirs, remove
from os.path import join, exists, isdir


def song_exists(song_title, playlist_name, music_base_path, special_playlist):
    song_path = join(get_song_path(playlist_name, music_base_path, special_playlist), song_title)
    to_remove_song=False
    if exists(song_path + '.mp3'):
        if exists(song_path  + '.webm'):
            remove(song_path + '.webm')
            to_remove_song=True
        if exists(song_path  + '.jpg'):
            remove(song_path + '.jpg')
            to_remove_song=True
        if exists(song_path  + '.webm.part'):
            remove(song_path + '.webm.part')
            to_remove_song=True
        if exists(song_path  + '.part'):
            remove(song_path + '.part')
            to_remove_song=True
        if to_remove_song:
            remove(song_path + '.mp3')
            return False
        else:
            return True
    else:
        return False

def get_song_path(playlist_name, music_base_path, special_playlist):
    if playlist_name in special_playlist:
        song_path = reduce(join, [music_base_path, str(datetime.now().year),
                                  '{} {}'.format(datetime.now().year, _get_season())])
    else:
        song_path = join(music_base_path, playlist_name)
    if not isdir(song_path):
        makedirs(song_path)
    return song_path


def _get_season():
    month = datetime.now().month
    if month == 12 or month < 3:
        return 'tel'
    elif 2 < month < 6:
        return 'tavasz'
    elif 5 < month < 9:
        return 'nyar'
    else:
        return 'osz'
