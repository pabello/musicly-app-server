from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from json import loads as load_json
from ..models import Artist, Recording
from ..serializers import ArtistSerializer, ArtistDetailsSerializer, RecordingSerializer, RecordingDetailsSerializer


class ArtistViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        stage_name = load_json(request.body)['stage_name']
        artists = get_list_or_404(Artist, stage_name__icontains=stage_name)
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        serializer = ArtistDetailsSerializer(artist)
        return Response(serializer.data)


class RecodingViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        title = load_json(request.body)['title']
        recordings = get_list_or_404(Recording, title__icontains=title)
        serializer = RecordingSerializer(recordings, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk):
        recording = get_object_or_404(Recording, pk=pk)
        serializer = RecordingDetailsSerializer(recording)
        return Response(serializer.data)

# TODO: when searching return both artists and recordings - its more practical