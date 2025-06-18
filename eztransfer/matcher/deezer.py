import requests

__name__ = '__get_deezer__'

def get_deezer_user(user_id:int):
    url = f"https://api.deezer.com/user/{user_id}"
    response = requests.get(url).json()

    user_dict = {
        'id':response['id'],
        'name':response['name'],
        'picture_small':response['picture_small']
    }
    return user_dict

def get_deezer_playlists_user(user_id:int):

    playlist_full = []
    url = f"https://api.deezer.com/user/{user_id}/playlists"
    while url:
        response = requests.get(url).json()

        for playlist in response.get('data'):
            playlist_full.append(playlist)

        url = response.get('next', None)
    return playlist_full


#procurando as músicas no deezer
def get_deezer_playlist_tracks(playlist_id:int):
    url = f"https://api.deezer.com/playlist/{playlist_id}/tracks"
    tracks = []
    response = requests.get(url).json()
    total = response['total']
    elapsed = 0
    x = 0
    print('Coletando músicas...')

    while url:
        response = requests.get(url).json()

        for track in response['data']:
            tracks.append({
                'title': track['title_short'].strip().lower(),
                'artist': track['artist']['name'].strip().lower(),
                'duration': track['duration']
            })
            elapsed += 1
            x = round(elapsed/total * 100)

            print(f"[{'#'*(x//4)}{' '*(25-x//4)}] ({x}%)", end='\r')

        url = response.get('next', None)
    print('\n')
    return tracks