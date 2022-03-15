import difflib
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
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


@api_view(['POST'])
def search_music_or_artist(request):
    key_word = request.data['search_phrase']

    recordings_queryset = Recording.objects.filter(
        # Q(title__icontains=key_word) | Q(artists_list__stage_name__icontains=key_word))
        Q(title__icontains=key_word))
    recordings = RecordingSerializer(recordings_queryset, many=True).data
    for recording in recordings:
        recording['name'] = recording.pop('title', None)
        recording['type'] = 'recording'
        recording['length'] = recording.pop('length', None)

    artists_queryser = Artist.objects.filter(stage_name__icontains=key_word)
    artists = ArtistSerializer(artists_queryser, many=True).data
    for artist in artists:
        artist['name'] = artist.pop('stage_name', None)
        artist['type'] = 'artist'

    merged = artists + recordings
    ordered = sorted(merged, key=lambda x: difflib.SequenceMatcher(None, x['name'], key_word).ratio(), reverse=True)

    return Response(status=status.HTTP_200_OK, data=ordered)
