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
        "redirect_url": "https://localhost:8000/",
        "scope": "user-read-private user-read-email"
    }

    response = requests.request(
        "GET", url="https://accounts.spotify.com/authorize", params=params, )
    return Response(response)
