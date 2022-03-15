from ..models import Account, Recording, UserMusic
from ..serializers import UserMusicSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import DatabaseError
from django.utils.timezone import now
from json import loads as load_json

from ..utils import unpack_common_filters


@api_view(['GET', 'POST'])
def user_music_list(request):
    like_status = None
    order_by, top = unpack_common_filters(request, 'music')

    if request.body:
        params = load_json(request.body)
        if 'like_status' in params.keys():
            if params['like_status'] == 'like':
                like_status = 1
            elif params['like_status'] == 'dislike':
                like_status = -1
            elif params['like_status'] == 'neutral':
                like_status = 0

    if like_status is not None:
        user_music = UserMusic.objects.filter(account=request.user, like_status=like_status).order_by(order_by)[:top]
    else:
        user_music = UserMusic.objects.filter(account=request.user).exclude(like_status=0).order_by(order_by)[:top]
    serializer = UserMusicSerializer(user_music, many=True)
    data = serializer.data

    for instance in data:
        recording = Recording.objects.get(pk=instance['recording_id'])
        instance['recording_title'] = recording.title
        instance['recording_length'] = recording.length
    return Response(data)


@api_view(['GET', 'POST'])
def music_reaction(request, pk):
    if request.method == 'GET':
        return get_music_reaction(request, pk)
    elif request.method == 'POST':
        return add_music_reaction(request, pk)
    else:
        return Response(status=status.HTTP_403_NOT_FOUND, data={'details': 'invalid request type.'})


def get_music_reaction(request, pk):
    try:
        user_music = UserMusic.objects.get(account=request.user, recording_id=pk)
        serializer = UserMusicSerializer(user_music, many=False)
        data = serializer.data
        return Response(data)
    except UserMusic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'details': 'like status does not exist.'})


def add_music_reaction(request, pk):
    try:
        user_music = UserMusic.objects.get(account=request.user, recording_id=pk)
        user_music.like_status = request.data['like_status']
        user_music.status_timestamp = now()
    except UserMusic.DoesNotExist:
        user_music = UserMusic.objects.create(account=request.user, recording_id=pk,
                                              like_status=request.data['like_status'])

    try:
        user_music.save()
        user_music_id = user_music.id
    except DatabaseError:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'details': 'server error, could not change like status.'})
    return Response(status=status.HTTP_200_OK, data={'details': 'like status changed.',
                                                     'user_music_id': user_music_id})
