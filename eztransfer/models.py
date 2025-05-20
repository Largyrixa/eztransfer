# models.py
from dataclasses import dataclass

@dataclass
class Track:
    id: str
    title: str
    artist: str
    duration: float
    popularity: int = 0
    album: str = None