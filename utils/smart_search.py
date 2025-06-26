import tidalapi
from rapidfuzz import fuzz

def search_track_tidal(session: tidalapi.Session, og_track: dict):
    def filter_results ():
        best_match_data = None
        high_score = -1.0
        for track in results['tracks']:
            if not (track.id and track.name and track.duration and track.artist and track.artist.name):
                continue
            
            track_score_components = {
                'id': str(track.id),
                'title': fuzz.token_sort_ratio(og_title_norm, track.name.lower(), score_cutoff=75),
                'artist': fuzz.token_set_ratio(og_artist_norm, track.artist.name.lower(), score_cutoff=85),
                'duration': (min(og_duration, track.duration) / max(og_duration, track.duration)) * 100,
                'popularity': track.popularity / 10
            }
            
            if track_score_components['artist'] < 85 or track_score_components['title'] < 75:
                continue
        
            current_score = 0
            for key, weight in pesos.items():
                current_score += track_score_components[key] * weight
            
            current_score /= 100
            
            if current_score > high_score:
                high_score = current_score
                best_match_data = track_score_components
                best_match_data['total'] = high_score
            elif current_score == high_score:
                if best_match_data and track_score_components['artist'] > best_match_data['artist']:
                    best_match_data = track_score_components
                    best_match_data['total'] = high_score
                    
        if best_match_data:
            return best_match_data['id']
        return None
    
    norm_table = {
        'я':'r',
        # Adicionar mais conforme necessário...
    }
    
    for old, new in norm_table.items():
        og_artist_norm = og_track['artist'].lower().replace(old, new)
        og_title_norm = og_track['title'].lower().replace(old, new)
                
    artist_mapping = {
        'chico buarque de hollanda': 'chico',
        'the smashing pumpkins': 'smashing pumpkins',
        '✝✝✝ (Crosses)': 'crosses'
        # Adicionar mais conforme necessário...
    }    
    
    for old, new in artist_mapping.items():
        if og_artist_norm == old:
            og_artist_norm = new
    
    # não gosto mais da shakira, depois eu tiro
    if og_artist_norm == 'shakira': 
        return None
    
    og_duration = og_track['duration']

    pesos = {
        'title': 45,
        'artist': 35,
        'duration': 15,
        'popularity': 5
    }

    # Primeira busca - Somente o nome
    results = session.search(
        f"{og_title_norm}",
        models=[tidalapi.Track],
        limit=20
    )
    
    if not results['tracks']:
        return None
    
    best_match_id = filter_results()
    
    if best_match_id:
        return best_match_id
    
    # Segunda busca - Nome + Artista
    # Essa busca pode ser feita de duas formas:
    # i - "nome - artista"
    
    results = session.search(
        f"{og_title_norm} - {og_artist_norm}",
        models=[tidalapi.Track],
        limit=10
    )
    
    best_match_id = filter_results()
    
    if best_match_id:
        return best_match_id
    
    # ii - "artista - nome"
    # como algumas músicas podem ter melhores resultados de acordo com a forma que é feita a busca
    # utilizaremos as duas formas, para melhorar a precisão
    # OBS: A maior parte da lentidão deve-se a um problema de I/O da API
    
    results = session.search(
        f"{og_artist_norm} - {og_title_norm}",
        models=[tidalapi.Track],
        limit=10
    )
    
    best_match_id = filter_results()
          
    if best_match_id:
        return best_match_id
                
    return None
