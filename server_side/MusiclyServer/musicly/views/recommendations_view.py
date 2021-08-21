from ..models import Recording, Account, UserMusic
from ..serializers import RecordingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


def get_recommendation_list(user):
    # TODO: implement an actual algorithm
    user_music = UserMusic.objects.filter(account=user)
    niemozliwe = [Recording.objects.get(pk=19844350)]  # TODO remove this and... well whatever. There should be a real algorithm anyway...
    recommendations = list(Recording.objects.all().exclude(pk__in=user_music)[:20])
    return niemozliwe + recommendations


@api_view(['GET'])
def recommendation_list(request):
    recommendations = get_recommendation_list(request.user)
    serializer = RecordingSerializer(recommendations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def next_recommendation(request):
    recommendation = get_recommendation_list(request.user)[0]
    serializer = RecordingSerializer(recommendation)
    return Response(serializer.data)