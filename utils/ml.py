from math import sqrt
import tensorflow_hub as hub

def get_vector_distance(v1: float, v2: float) -> float:
    distance1 = sqrt(sum(x**2 for x in v1))
    distance2 = sqrt(sum(x**2 for x in v2))

    return distance1 - distance2

def get_phrase_and_song_similarity(phrase: str, song_id: str):
    song_lyrics = "" # get song lyrics from scraping

    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    phrase_vector = embed([phrase]).numpy()
    lyrics_vector = embed([song_lyrics]).numpy()

    return abs(get_vector_distance(phrase_vector, lyrics_vector))

def is_phrase_and_song_similar(phrase: str, song_id: str, threshold: float) -> bool:
    if (get_phrase_and_song_similarity(phrase, song_id) <= threshold):
        return True

    return False
