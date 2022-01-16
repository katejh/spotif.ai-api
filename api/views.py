import asyncio
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from dotenv import load_dotenv
import os

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

    dummy_data = {"songs": [1, 2, 3, 4]}

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

    response = requests.get(
        url="https://accounts.spotify.com/authorize", params=params)


@api_view(["POST"])
def get_songs(request):
    token = request.data.token

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        "https://api.spotify.com/v1/me/playlists", headers=headers)

    if not response:
        return Response(data="Could not get playlists", status=502)

    information = response.json()

    playlists = []

    for playlist in information["items"]:
        id = playlist["id"]
        name = playlist["name"]

        song_response = requests.get(
            f"https://api.spotify.com/v1/playlists/{id}/tracks?market=US", headers=headers)

        if not song_response:
            return Response(data="Could not get song response", status=502)

        song_info = song_response.json()

        songs = []
        for item in song_info["items"]:
            song_artist = item["track"]["artists"][0]["name"]
            song_name = item["track"]["name"]
            external_url = item["track"]["external_urls"]["spotify"]
            album = item["track"]["images"][0]

            songs.append({
                "artist": song_artist,
                "name": song_name,
                "external_url": external_url,
                "album": album
            })

        playlists.append({
            name: songs
        })

    return Response(data={"playlists": playlists}, status=200)
