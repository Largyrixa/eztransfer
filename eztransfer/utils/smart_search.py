import tidalapi
from rapidfuzz import fuzz

def search_track_tidal(session:tidalapi.Session, og_track:dict):
    high_score = -1
    best_match = None
    og_track['artist'] = og_track['artist'].replace('я', 'r')
    og_track['title']  = og_track['title'].replace('я', 'r')
    
    if og_track['artist'] == 'the smashing pumpkins': og_track['artist'] = 'smashing pumpkins'
    
    pesos = {
        'title'     :45,
        'artist'    :35,
        'duration'  :15,
        'popularity':5
    }
    
    results = session.search(f"{og_track['title']} {og_track['artist']}", models=[tidalapi.Track], limit=10)
    
    if not results['tracks']:
        return None
    
    for track in results['tracks']:
        track_score = {
            'id': track.id,
            'title': fuzz.ratio(og_track['title'], track.name.lower()),
            'artist': fuzz.ratio(og_track['artist'], track.artist.name.lower()),
            'duration': 100*(min(og_track['duration'],track.duration) / max(og_track['duration'],track.duration)),
            'popularity': track.popularity*10
        }
        
        current_score = 0
        for key, weight in pesos.items():
            current_score += track_score[key] * weight
            
        current_score /= 100
        
        if current_score > high_score:
            high_score = current_score
            best_match = track_score
            best_match['total'] = current_score
        elif current_score == high_score:
            if best_match and track_score['artist'] > best_match['artist']:
                best_match = track_score
                best_match['total'] = high_score
                
    if not best_match:
        return None
            
    return best_match['id']