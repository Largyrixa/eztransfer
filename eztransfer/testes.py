import requests
import tidalapi
import webbrowser as web

def format_string(string:str):
    invalid_chars = [
        '(',')','[',']','{','}','!','?', '_', '-'
    ]
    invalid_strs = [
        'live', 'remastered', 'feat', 'ft', 'ft.'
    ]

    string = string.lower()

    # remoção de caracteres inválidos:
    for i_char in invalid_chars:
        string = string.replace(i_char, ' ')

    if 'Я' in string:
        string = string.replace('Я', 'r')

    # remoção de strings inválidas
    string = string.strip().split()
    for i, word in enumerate(string):
        if word in invalid_strs:
            string.pop(i)
    
    return ''.join(string)

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
    print('Procurando músicas...')

    while url:
        response = requests.get(url).json()

        for track in response['data']:
            tracks.append({
                'title':  format_string(track['title_short']),
                'artist': format_string(track['artist']['name']),
                'duration': track['duration']
            })
            elapsed += 1
            x = round(elapsed/total * 100)

            print(f'[{'#'*(x//4)}{' '*(25-(x//4))}] {x}%', end='\r')


        url = response.get('next', None)
    print()
    return tracks

#procurando as músicas no Tidal e adicionar à playlist
def add_tracks_to_tidal_playlist(tracks:list, tidal_playlist_name:str, session:tidalapi.Session):
    # Criar uma nova playlist
    playlist = session.user.create_playlist(tidal_playlist_name,'')

    # Procurar e adicionar músicas
    total = len(tracks)
    elapsed = 0
    erros = 0
    nao_achou = []
    achou = []
    
    print(f'Criando "{tidal_playlist_name}"...')
    for track in tracks:
        track_found = False # achei que essa lógica fosse melhor
        search_results = session.search(f"{track['title']} {track['artist']}", models=[tidalapi.Track])

        if len(search_results['tracks']) > 0:
            # filtrando os resultados pela duração da música (com diferença de até 3 segundos)
            for i in range(len(search_results['tracks'])):
                if search_results['tracks'][i].duration in range(track['duration']-3, track['duration']+4):
                    # mantive o try-except para evitar crashs, mas tirei a contagem de erros para esse caso
                    try:
                        achou.append(search_results['tracks'][i].id)
                        track_found=True
                        break
                    except Exception as e:
                        continue
                
        if not track_found:
            nao_achou.append(track)
            erros += 1

        elapsed += 1
        x = round(elapsed/total * 100)

        print(f'[{'#'*(x//4)}{' '*(25-(x//4))}] {x}%', end='\r')
    print()

    playlist.add(achou) # melhor fazer uma chamada para a api que adiciona todas as músicas

    print(f"Playlist '{tidal_playlist_name}' criada no Tidal!")
    print(f"{f'{(1-erros/len(tracks))*100:.2f}'} % de sucesso")
    
    r = input('ver as músicas não encontradas? (S/n)\n>>>') if len(nao_achou) > 0 else 'n'

    if r.lower().strip() in ('s', ''):
        for i in range(len(nao_achou)):
            input(nao_achou[i])

if __name__ == "__main__":
    session = tidalapi.Session()
    login, future = session.login_oauth()
    print('Você será redirecionado à página de login do Tidal para começar.')
    web.open(login.verification_uri_complete)

    user_id = input('Informe o seu ID da Deezer: ')

    # Dados do usuário do Deezer
    # user_id = 1097864826 # mensageirodobem
    # user_id = 4873742222 # Calangolango

    user = get_deezer_user(user_id=user_id)
    playlists = get_deezer_playlists_user(user_id=user_id)

    print(f'''
          Você é {user["name"]} - {user["id"]}
          '''
          ) # utilizar a user['picture'] somente na implementação web
    resposta = 's'
    while resposta in ('s', ''):
        for playlist in playlists:
            add = input(f'Deseja adicionar a playlist {playlist["title"]} - {playlist["id"]} - {playlist["nb_tracks"]} músicas? (S=sim/n=não/q=sair)\n>>>').lower().strip()
                #     r = input(f'a playlist achada têm {len(tracks)} músicas, confere? (S/n)\n>>>')
            if add != 's' and add != '':
                continue
            if add == 'q':
                break
        
            tracks = get_deezer_playlist_tracks(playlist["id"])
            tidal_playlist_name = input("Insira o nome da playlist a ser criada no Tidal\n>>>")
            add_tracks_to_tidal_playlist(tracks, tidal_playlist_name, session)
        resposta = None