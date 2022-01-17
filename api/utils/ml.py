from math import sqrt
import requests
import string
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def get_vector_distance(v1, v2) -> float:
    """ Calculates Euclidean distance between the two 512-dimension vectors
    """
    sum = 0

    for i in range(512):
        sum += (v1[0][i] - v2[0][i])**2

    return sqrt(sum)

def convert_texts_to_vector(texts: str) -> [int]:
    """ Pings Colab endpoint to turn texts into 512-dimension unit vectors
    """
    data = {"texts": texts}

    r = requests.get(os.environ.get("COLAB_SERVER_URL") + "/vector", json=data)
    r = r.json()
    return r["vectors"]

def get_phrase_and_songs_similarity(phrase: str, songs: [str]) -> [int]:
    """ Calculates the similarity between songs and the inputted phrase
    """

    phrase_vector = convert_texts_to_vector([phrase])[0]
    songs_vector = convert_texts_to_vector(songs)


    distances = []

    for vector in songs_vector:
        distances.append(abs(get_vector_distance(phrase_vector, vector)))

    return distances

def get_similar_songs(phrase: str, songs: str, threshold: float, limit=50) -> [int]:
    """ Uses the song_info to calculate how close each is to the phrase, the similar ones as indices
    """
    indices = []
    count = 0

    distances = get_phrase_and_songs_similarity(phrase, songs)

    for i in range(len(distances)):
        logging.info(f"checking song {i}")
        if distances[i] <= threshold:
            indices.append(i)
            logging.info(f"added song {i}, {count} songs added so far")

            count += 1

            if count >= limit:
                break

    return indices
