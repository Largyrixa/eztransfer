import tidalapi
from utils.smart_search import *
from time import sleep

__name__ = '__to_tidal__'

#procurando as músicas no Tidal e adicionar à playlist
def add_tracks_to_tidal_playlist(tracks:list, tidal_playlist_name:str, session:tidalapi.session.Session):
    # Criar uma nova playlist
    playlist = session.user.create_playlist(tidal_playlist_name,'')

    # Procurar e adicionar músicas
    total = len(tracks)
    elapsed = 0
    nao_achou = []
    achou = []
    
    print(f'Criando "{tidal_playlist_name}"...')
    for track in tracks:        
        matched_track = search_track(session, track)
        if len(achou) >= 100:
            # Não sei o porquê, mas quando você deixa allow_duplicates=True, ele tem uma taxa de sucesso mais alta
            playlist.add(achou, allow_duplicates=False)
            achou = []

        if matched_track:
            try:
                achou.append(matched_track.id)
            except Exception as e:
                sleep(1)
                continue
        else:
            nao_achou.append(track)

        elapsed += 1
        x = round(elapsed/total * 100)

        print(f'[{'#'*(x//4)}{' '*(25-(x//4))}] {x}%', end='\r')
    print('\n')

    if len(achou) > 0:
        playlist.add(achou,allow_duplicates=False)

    erros = len(nao_achou)

    print(f"Playlist '{tidal_playlist_name}' criada no Tidal!")
    print(f"{f'{(1-erros/elapsed)*100:.2f}'} % de sucesso\n")
    
    r = input('ver as músicas não encontradas? (S/n)\n>>>') if erros > 0 else 'n'

    if r.lower().strip() in ('s', ''):
        for i in range(len(nao_achou)):
            input(nao_achou[i])
    print()
