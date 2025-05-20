from fuzzywuzzy import fuzz
import tidalapi
import re

def find_best_match(results:list[tidalapi.Track], original_track:dict):
    if not results:
        return None
    
    # Filtrando os resultados pelo nome do artista
    artist = max(results, key=lambda x:
        fuzz.partial_ratio(x.artist.name.lower(), original_track['artist'])
    ).artist.name

    results = [
        t for t in results
        if t.artist.name == artist
    ]

    # Primeiro: procurar por duração exata ou muito próxima
    exact_duration_matches = [
        t for t in results
        if abs(t.duration - original_track['duration']) <= 2.5
    ]

    if exact_duration_matches:
        # Entre as de duração correta, pegar a mais popular
        return max(exact_duration_matches, key=lambda x: x.popularity)

    # Se não encontrar, pegar a mais popular com título similar
    return max(results, key=lambda x: (
        fuzz.partial_ratio(x.name.lower(), original_track['title'].lower()) +
        fuzz.partial_ratio(x.artist.name.lower(), original_track['artist'].lower())
    ))

def search_track(session, track:dict):
    formating_table = {
            '&': 'e',
            'я': 'r'
    }
    track['title'] = track['title'].lower()
    track['artist'] = track['artist'].lower()
    for k, v in formating_table.items():
        track['artist']=track['artist'].replace(k, v)
        track['title']=track['title'].replace(k, v)

    # Tentativa 1: Busca exata com formatação padrão
    results = session.search(f'{track['title']}', models=[tidalapi.Track])['tracks']
    if match := find_best_match(results, track):
        return match

    # Tentativa 2: Removendo parênteses e tags
    clean_title = re.sub(r'\([^)]*\)|\[[^\]]*\]', '', track['title']).strip()
    results = session.search(f"{clean_title}", models=[tidalapi.Track])['tracks']
    if match := find_best_match(results, track):
        return match
    
    # Tentativa 3: Apenas artista + título principal
    main_title = track['title'].split('-')[0].strip()
    results = [t for t in session.search(f"{main_title}", models=[tidalapi.Track])['tracks']
                if t.artist.name == track['artist']]
    if match := find_best_match(results, track):
        return match