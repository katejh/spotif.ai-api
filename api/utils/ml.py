from math import sqrt
import requests
import string
import os

def get_vector_distance(v1, v2) -> float:
    sum = 0
    for i in range(512):
        sum += (v1[i] - v2[i])**2

    return sqrt(sum)

def convert_text_to_vector(text: str):
    data = {"text": text}

    r = requests.get(os.environ.get("COLAB_SERVER_URL") + "/vector", json=data)

    r = r.json()

    print(r)

    return r["vector"]

def get_phrase_and_song_similarity(phrase: str, song_id: str) -> float:
    # get song lyrics from scraping
    song_lyrics = "the cold never bothered me anyway"
    

    # convert to vectors
    phrase_vector = convert_text_to_vector(phrase)
    lyrics_vector = convert_text_to_vector(song_lyrics)

    return abs(get_vector_distance(phrase_vector, lyrics_vector))

def is_phrase_and_song_similar(phrase: str, song_id: str, threshold: float) -> bool:
    if (get_phrase_and_song_similarity(phrase, song_id) <= threshold):
        return True

    return False
