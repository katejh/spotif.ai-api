from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
 

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
    