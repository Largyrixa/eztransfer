from matcher import deezer, tidal, spotify

logo = \
"""
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ ███████╗███████╗████████╗██████╗  █████╗ ███╗   ██╗███████╗███████╗███████╗██████╗  │
│ ██╔════╝╚══███╔╝╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝██╔════╝██╔══██╗ │
│ █████╗    ███╔╝    ██║   ██████╔╝███████║██╔██╗ ██║███████╗█████╗  █████╗  ██████╔╝ │
│ ██╔══╝   ███╔╝     ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██╔══╝  ██╔══╝  ██╔══██╗ │
│ ███████╗███████╗   ██║   ██║  ██║██║  ██║██║ ╚████║███████║██║     ███████╗██║  ██║ │
│ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝ │
└─────────────────────────────────────────────────────────────────────────────────────┘
"""



if __name__ == "__main__":
  print(logo)
  
  print(">>> SELECIONE O SERVIÇO DE RETIRADA <<<")
  print("[1] Deezer")
  print("[2] Spotify")
  print("[3] Tidal")
  print("[q] Sair")
  retirada = input(">>> ").strip().lower()
  
  if retirada == 'q':
    exit()
  
  print("\n>>> SELECIONE O SERVIÇO DE DESTINO <<<")
  print("[1] Deezer")
  print("[2] Spotify")
  print("[3] Tidal")
  print("[q] Sair")
  chegada = input(">>> ").strip().lower()
  
  if chegada == retirada:
    print("> Os serviços não podem ser os mesmos!\nSaindo do programa...")
    exit()

  if chegada == 'q':
    exit()
    
  match retirada+chegada:
    #case '12':
    #
    
    case '13':
      deezer_user   = deezer.get_deezer_user(input("Insira seu ID de usuário da Deezer\n>>> ").strip())
      tidal_session = tidal.get_session()
      playlists     = deezer.get_deezer_playlists_user(deezer_user)
      
      print("\n>>> ESCOLHA AS PLAYLISTS QUE QUER TRANSFERIR <<<")
      for playlist in playlists:
        print(f"> {playlist["name"]} - {len(playlist["tracks"])} músicas? (s/N)")
        decisao = input(">>> ").lower().strip()

        if decisao == 's':
          tidal.transfer_playlist(playlist, tidal_session)

    #case '21':
    #
    #case '23':
    #
    #case '31':
    #
    case '32':
      tidal_session   = tidal.get_session()
      spotify_session = spotify.get_session()
      
      playlists = tidal.get_playlists(tidal_session)
      
      print("\n>>> ESCOLHA AS PLAYLISTS QUE QUER TRANSFERIR <<<")
      for i, playlist in enumerate(playlists):
        print(f"> {playlist["name"]} - {len(playlist["tracks"])} músicas? (s/N)")
        decisao = input(">>> ").lower().strip()
        
        if decisao == 's':
          spotify.transfer_playlist(spotify_session, playlist)
    
    case _:
      print("Ainda em desenvolvimento...")

