import webbrowser as web
import tidalapi
from matcher.deezer import *
from matcher.tidal import *

if __name__ == '__main__':
    session = tidalapi.Session()
    login, future = session.login_oauth()
    print('Você será redirecionado à página de login do Tidal para começar.')
    web.open(login.verification_uri_complete)

    user_id = input('Informe o seu ID da Deezer: ')

    # Dados do usuário do Deezer
    # user_id = 1097864826 # mensageirodobem
    user_id = 4873742222 # Calangolango

    user = get_deezer_user(user_id=user_id)
    playlists = get_deezer_playlists_user(user_id=user_id)

    print(f'''
          Você é {user["name"]} - {user["id"]}
          '''
          ) # utilizar a user['picture'] somente na implementação web
    for playlist in playlists:
        add = input(f'Deseja adicionar a playlist {playlist["title"]} - {playlist["id"]} - {playlist["nb_tracks"]} músicas? (s=sim/N=não/q=sair)\n>>>').lower().strip()
            #     r = input(f'a playlist achada têm {len(tracks)} músicas, confere? (S/n)\n>>>')
        
        if add == 'q':
            break

        if add != 's':
            continue
    
        tracks = get_deezer_playlist_tracks(playlist["id"])
        tidal_playlist_name = input("Insira o nome da playlist a ser criada no Tidal\n>>>")
        add_tracks_to_tidal_playlist(tracks, tidal_playlist_name, session)
