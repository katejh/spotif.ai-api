import asyncio
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from dotenv import load_dotenv
import os
import random
from utils.scrappers import get_lyrics, clean_text
from utils.ml import is_phrase_and_song_similar

load_dotenv()

@api_view(['GET'])
def dummy(request):
    return Response(200)


@api_view(['GET'])
def dummy_get(request, num):
    return Response(f"Input: {num}")


@api_view(['POST'])
def dummy_post(request):
    prompt = request.data.get("prompt")
    token = request.data.get("token")
    response = f"you said {prompt} and {token}"
    print(response)
    
    dummy_data = {"songs": [1,2,3,4]}
    
    
    return Response(dummy_data)


@api_view(["GET"])
def login(request):

    params = {
        "response_type": "code",
        "client_id": "dfda70caf6ae465a95ce18a61dc47623",
        "redirect_url": "https://localhost:8000/login",
        "scope": "user-read-private user-read-email",
        "show_dialog": True
    }

    response = requests.get(url="https://accounts.spotify.com/authorize", params=params)


@api_view(["GET"])
def provide_auth_token(request):
    global auth_token
    auth_token = request.GET.get("auth_token")


@api_view(["POST"])
def get_songs(request):
<<<<<<< HEAD
    token = request.token
=======
    playlists = fetch_songs_from_playlists()

    return Response(data={"playlists": playlists}, status=200)

def fetch_songs_from_playlists():
    token = os.environ.get("SPOTIFY_BEARER_TOKEN")
>>>>>>> ml created playlist prototype because the last commit was wack
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

    if not response:
        return Response(data="Could not get playlists", status=502)

    information = response.json()

    playlists = []

    for playlist in information["items"]:
        id = playlist["id"]
        name = playlist["name"]

        song_response = requests.get(f"https://api.spotify.com/v1/playlists/{id}/tracks?market=US", headers=headers)

        if not song_response:
            return Response(data="Could not get song response", status=502)

        song_info = song_response.json()

        songs = []
        for item in song_info["items"]:
            song_artist = item["track"]["artists"][0]["name"]
            song_name = item["track"]["name"]
            song_id = item["track"]["id"]
            song_artist_id = item["track"]["artists"][0]["id"]
            songs.append({
                "artist": song_artist,
                "name": song_name,
                "id": song_id,
                "artist_id": song_artist_id
            })

        playlists.append({
            name: songs
        })
    
    return playlists

def create_playlist(phrase, limit=50):
    token = os.environ.get("SPOTIFY_BEARER_TOKEN")

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    playlists = fetch_songs_from_playlists()

    songs = []

    for playlist in playlists:
        for song in playlist[list(playlist.keys())[0]]:
            songs.append(song)

    tracks_response = requests.get("https://api.spotify.com/v1/me/tracks", headers=headers)
    tracks_response_json = tracks_response.json()

    for song in tracks_response_json["items"]:
        song_artist = song["track"]["artists"][0]["name"]
        song_artist_id = song["track"]["artists"][0]["id"]
        song_name = song["track"]["name"]
        song_id = song["track"]["id"]
        songs.append({
            "artist": song_artist,
            "name": song_name,
            "id": song_id,
            "artist_id": song_artist_id
        })

    # get some recommended songs too
    params = {
        "seed_tracks": [random.choice(songs)["id"] for i in range(3)],
        "seed_artists": [random.choice(songs)["artist_id"] for i in range(2)]
    }

    suggestions_response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers)
    suggestions_response_json = suggestions_response.json()

    for song in suggestions_response_json["tracks"]:
        artist = song["artists"][0]["name"]
        artist_id = song["artists"][0]["id"]
        name = song["name"]
        id = song["id"]
        songs.append({
            "artist": artist,
            "artist_id": artist_id,
            "name": name,
            "id": id
        })

    matching_songs = []

    for song in songs:
        # through tests threshold of 1 seems good
        lyrics = get_lyrics(song["name"], song["artist"])
        if is_phrase_and_song_similar(clean_text(phrase), lyrics, 1.0):
            matching_songs.append(song)

    random.shuffle(matching_songs)
    return matching_songs[:limit]
