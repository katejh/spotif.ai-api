from math import sqrt
import requests
import string
import os
from dotenv import load_dotenv

load_dotenv()

def get_vector_distance(v1, v2) -> float:
    sum = 0
    # print(v1)
    # print(v2)

    for i in range(512):
        sum += (v1[0][i] - v2[0][i])**2

    return sqrt(sum)

def convert_texts_to_vector(texts: str):
    # print(text)
    data = {"texts": texts}

    r = requests.get(os.environ.get("COLAB_SERVER_URL") + "/vector", json=data)
    # print(r)
    r = r.json()
    # print(r)

    return r["vectors"]

def get_phrase_and_songs_similarity(phrase: str, song_lyrics):
    # convert to vectors
    phrase_vector = convert_texts_to_vector([phrase])[0]
    lyrics_vector = convert_texts_to_vector(song_lyrics)

    # print(lyrics_vector)

    distances = []

    # print(phrase_vector)
    # print(lyrics_vector)

    for lyric_vector in lyrics_vector:
        distances.append(abs(get_vector_distance(phrase_vector, lyric_vector)))

    return distances

def get_similar_songs(phrase: str, song_lyrics: str, threshold: float, limit=50):
    print('did we get here')
    indices = []
    count = 0

    distances = get_phrase_and_songs_similarity(phrase, song_lyrics)

    for i in range(len(distances)):
        print(f"checking song {i}")
        if distances[i] <= threshold:
            indices.append(i)
            print(f"added song {i}, {count} songs added so far")

            if count >= threshold:
                break

    return indices
