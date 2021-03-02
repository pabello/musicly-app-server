from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from json import loads as load_json
from ..models import Playlist, PlaylistMusic
from ..serializers import PlaylistSerializer, PlaylistMusicSerializer


class PlaylistViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        # TODO: Get user id by token
        account_id = load_json(request.body)['account_id']
        playlists = get_list_or_404(Playlist, account_id=account_id)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)
        serializer = PlaylistMusicSerializer(playlist)
        return Response(serializer.data)
