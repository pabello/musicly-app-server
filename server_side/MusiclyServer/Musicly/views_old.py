from django.http import JsonResponse
import json
from rest_framework.response import Response


def headers(request):
    return Response(request)


def json_input(request):
    return JsonResponse(json.loads(request.body))
