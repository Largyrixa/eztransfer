import tidalapi
from utils.smart_search import search_track_tidal
from time import sleep

def add_tracks_to_tidal_playlist(tracks:list, tidal_playlist_name:str, session:tidalapi.session.Session):
    # Criar uma nova playlist
    playlist = session.user.create_playlist(tidal_playlist_name,'')

    # Procurar e adicionar músicas
    total = len(tracks)
    elapsed = 0
    achou = []
    nao_achou = []
    
    print(f'Criando "{tidal_playlist_name}"')
    for track in tracks:        
        matched_track = search_track_tidal(session, track)
        
        if len(achou) >= 100:
            playlist.add(achou, limit = 100)
            achou = []
        
        if matched_track:
            achou.append(matched_track)
        else:
            nao_achou.append(track)

        elapsed += 1
        x = round(elapsed/total * 100)

        print(f'[{'#'*(x//4)}{' '*(25-(x//4))}] {x}%', end='\r')
    print('\n')
    playlist.add(achou, limit=(len(achou)+1))

    erros = len(nao_achou)

    print(f"Playlist '{tidal_playlist_name}' criada no Tidal!")
    print(f"{f'{(1-erros/len(tracks))*100:.2f}'} % de sucesso\n")
    
    r = input('ver as músicas não encontradas? (S/n)\n>>>') if erros > 0 else 'n'

    if r.lower().strip() in ('s', ''):
        for i in range(len(nao_achou)):
            input(nao_achou[i])
    print()
