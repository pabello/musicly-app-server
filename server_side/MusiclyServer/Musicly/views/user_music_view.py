from ..models import Account, Recording, UserMusic
from ..serializers import UserMusicSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def user_music_list(request):
    user_music = UserMusic.objects.filter(account=request.user)
    serializer = UserMusicSerializer(user_music, many=True)
    data = serializer.data

    for instance in data:
        title = Recording.objects.get(pk=instance['recording_id']).title
        instance['recording_title'] = title

    return Response(data)
