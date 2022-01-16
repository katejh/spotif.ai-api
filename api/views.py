import asyncio
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests


@api_view(['GET'])
def dummy(request):
    return Response(200)


@api_view(['GET'])
def dummy_get(request, num):
    return Response(f"Input: {num}")


@api_view(['POST'])
def dummy_post(request):
    uuid = request.data.get("number")
    return Response(uuid)


@api_view(["GET"])
def login(request):

    params = {
        "response_type": "code",
        "client_id": "dfda70caf6ae465a95ce18a61dc47623",
        "redirect_url": "https://localhost:8000/login",
        "scope": "user-read-private user-read-email",
        "show_dialog": True
    }

    response = requests.request(
        "GET", url="https://accounts.spotify.com/authorize", params=params)


@api_view(["GET"])
def provide_auth_token(request):

    global auth_token
    auth_token = request.GET.get("auth_token")


@api_view(["GET"])
def get_songs(request):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer BQBjltjj1KxABc4w_ckeqkrpXFpMGshNSA8QIGr3J3nUTWRRJH_ckg5sdOZkQ61vO_12NNgPLGRjC62Ui82DBANoi-VVt2RKvAP2hl2o0XjuEhvY_K_ctVG5RP1kJrZteEqNH4AMSP5xwHcpjzwqf08ie1nVQA'
    }

    response = requests.request(
        "GET", "https://api.spotify.com/v1/me/playlists", headers=headers)

    if not response:
        return Response(data="Error", status=502)

    information = response.json()

    playlists = []

    for playlist in information["items"]:
        id = playlist["id"]
        name = playlist["name"]

        song_response = requests.request(
            "GET", f"https://api.spotify.com/v1/playlists/{id}/tracks?market=US", headers=headers)

        if not song_response:
            return Response(data="Error", status=502)

        song_info = song_response.json()

        songs = []
        for item in song_info["items"]:
            song_artist = item["track"]["artists"][0]["name"]
            song_name = item["track"]["name"]
            songs.append({
                "artist": song_artist,
                "name": song_name
            })

        playlists.append({
            name: songs
        })

    return Response(data={"playlists": playlists}, status=200)
