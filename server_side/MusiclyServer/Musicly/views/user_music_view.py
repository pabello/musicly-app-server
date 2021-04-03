from ..models import Account, Recording, UserMusic
from ..serializers import UserMusicSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import DatabaseError


@api_view(['GET'])
def user_music_list(request):
    user_music = UserMusic.objects.filter(account=request.user)
    serializer = UserMusicSerializer(user_music, many=True)
    data = serializer.data

    for instance in data:
        title = Recording.objects.get(pk=instance['recording_id']).title
        instance['recording_title'] = title
    return Response(data)


@api_view(['POST'])
def add_music_reaction(request, pk):
    try:
        user_music = UserMusic.objects.get(account=request.user, recording_id=pk)
        user_music.like_status = request.data['like_status']
    except UserMusic.DoesNotExist:
        user_music = UserMusic.objects.create(account=request.user, recording_id=pk,
                                              like_status=request.data['like_status'], listen_count=0)

    try:
        user_music_id = user_music.save().id
    except DatabaseError:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'details': 'server error could not change like status.',
                              'user_music_id': user_music_id})
    return Response(status=status.HTTP_200_OK, data={'details': 'like status changed.'})
