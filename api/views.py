import asyncio
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from dotenv import load_dotenv
import os
import random
from .utils.scrappers import get_lyrics, clean_text
from .utils.ml import get_similar_songs
from .utils.helpers import get_user_playlists, get_user_songs, get_song_suggestions, get_user_id
import json

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
    playlists, status = get_user_playlists(request.data.get('token'))
    
    return Response(data=playlists, status=status)

@api_view(["POST"])
def create_playlist(request):
    token = request.data.get('token')
    phrase = request.data.get('phrase')
    limit = 50

    try:
        limit = int(request.data.get('limit'))
    except:
        None

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    songs = []

    playlists, status = get_user_playlists(token)
    user_tracks, status = get_user_songs(token)

    print('did we get here')

    # print(playlists)
    for playlist in playlists:
        # print(playlist)
        for song in playlist["songs"]:
            songs.append(song)

    for track in user_tracks:
        songs.append(track)

    suggestions, status = get_song_suggestions(token, seed_tracks=[random.choice(songs)["id"] for i in range(3)], seed_artists=[random.choice(songs)["artist_id"] for i in range(2)])
    print('did we get here')
    for track in suggestions:
        songs.append(track)

    songs_suggestions_weighted = [] # array with combined existing songs and suggested songs, with weight for each
    
    total_songs = len(songs) + len(suggestions)

    for song in songs:
        if random.randint(0,total_songs) <= 0.25 * total_songs:
            songs_suggestions_weighted.append(song)

    for song in suggestions:
        if random.randint(0,total_songs) <= 0.75 * total_songs:
            songs_suggestions_weighted.append(song)

    matching_songs = []
    count = 0

    lyrics = []
    titles = []

    print('did we get here')
    random.shuffle(songs_suggestions_weighted)
    for song in songs_suggestions_weighted:
        # lyrics.append(get_lyrics(song["name"], song["artist_name"]))
        titles.append(song["name"])

    print('did we get here')

    matching_indices = get_similar_songs(clean_text(phrase), titles, 1.25, limit)

    for i in matching_indices:
        matching_songs.append(songs_suggestions_weighted[i])

    return Response(data=matching_songs, status=200)

@api_view(["POST"])
def playlist(request):
    token = request.data.get("token")
    user_id = get_user_id(token)
    playlist_name = request.data.get("playlist_name")
    playlist_description = request.data.get("description")
    songs = request.data.get("songs")
    print(songs)

    payload = json.dumps({
        "name": playlist_name,
        "description": playlist_description,
        "public": False
    })

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    response = requests.request(
        "POST", f"https://api.spotify.com/v1/users/{user_id}/playlists", headers=headers, data=payload)

    if not response:
        return Response(data="Could not create a playlist", status=502)

    info = response.json()
    playlist_id = info["id"]

    #songs = songs.replace(":", "%3A")
    #songs = songs.replace(",", "%2C")
    songQuery = ",".join(songs)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    response = requests.request(
        "POST", f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={songQuery}", headers=headers, data={})
    if not response:
        print(response.text)
        return Response("failure", 502)
    return Response("success", 200)

