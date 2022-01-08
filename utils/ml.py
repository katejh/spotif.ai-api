from math import sqrt
import tensorflow_hub as hub

def get_vector_distance(v1: List[float], v2: List[float]) -> float:
    distance1 = sqrt(sum(x**2 for x in v1))
    distance2 = sqrt(sum(x**2 for x in v2))

    return distance1 - distance2

def get_phrase_and_song_similarity(phrase: str, song_id: str) -> float:
    song_lyrics = "" # get song lyrics from scraping

    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4") # preload tensorflow model

    # convert to vectors
    phrase_vector = embed([phrase]).numpy().tolist()
    lyrics_vector = embed([song_lyrics]).numpy().tolist()

    return abs(get_vector_distance(phrase_vector, lyrics_vector))

def is_phrase_and_song_similar(phrase: str, song_id: str, threshold: float) -> bool:
    if (get_phrase_and_song_similarity(phrase, song_id) <= threshold):
        return True

    return False
