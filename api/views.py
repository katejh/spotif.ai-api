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
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)



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


    for playlist in playlists:
        for song in playlist["songs"]:
            songs.append(song)

    for track in user_tracks:
        songs.append(track)

    suggestions, status = get_song_suggestions(token, seed_tracks=[random.choice(songs)["id"] for i in range(3)], seed_artists=[random.choice(songs)["artist_id"] for i in range(2)])

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

    random.shuffle(songs_suggestions_weighted)
    for song in songs_suggestions_weighted:
        titles.append(song["name"])

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
        logging.warning(f"Could not create playlist. Error: {response.text}")
        return Response(data="Could not create a playlist", status=502)
    info = response.json()
    playlist_id = info["id"]

    logging.info(f"Successfully created playlist {playlist_name}")

    songQuery = ",".join(songs)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    response = requests.request(
        "POST", f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={songQuery}", headers=headers, data={})
    if not response:
        logging.warning(f"Could not upload songs to the new playlist. Error: {response.text}")
        return Response("failure", 502)
    
    logging.info(f"Successfully uploaded songs to the new playlist")
    return Response("success", 200)

