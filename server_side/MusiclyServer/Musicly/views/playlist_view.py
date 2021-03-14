from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Playlist, PlaylistMusic, Recording
from ..serializers import PlaylistSerializer, PlaylistMusicSerializer, PlaylistMusicListSerializer
from django.db import transaction


def get_playlist_music_count(playlist: Playlist):
    playlist_music_list = PlaylistMusic.objects.filter(playlist=playlist)
    return len(playlist_music_list)


class PlaylistViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        playlists = get_list_or_404(Playlist, account_id=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)
        if playlist.account != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'not the owner of the playlist.'})
        serializer = PlaylistMusicListSerializer(playlist)
        print(serializer.data)
        return Response(serializer.data)

    @staticmethod
    def create(request):
        playlist_data = request.data
        playlist_data['account'] = request.user.id
        serializer = PlaylistSerializer(data=playlist_data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'details': 'playlist created.'})
        else:
            return Response(serializer.errors)

    @staticmethod
    def partial_update(request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)
        if playlist.account != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'not the owner of the playlist.'})

        new_name = request.data['name']
        playlist.name = new_name
        try:
            playlist.save()
            return Response(status=status.HTTP_200_OK, data={'details': 'playlist name updated.'})
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'details': 'server error, could not update the playlist.'})

    @staticmethod
    def delete(request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)
        if playlist.account != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'not the owner of the playlist'})

        try:
            playlist.delete()
            return Response(status=status.HTTP_200_OK, data={'details': 'playlist deleted.'})
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'details': 'server error, could not delete the playlist.'})


class APIInputException(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response


class PlaylistMusicViewSet(viewsets.ViewSet):
    @staticmethod
    def get_playlist_music_data(request, pk):
        try:
            playlist_music = PlaylistMusic.objects.get(pk=pk)
            playlist = Playlist.objects.get(pk=playlist_music.playlist_id)
        except PlaylistMusic.DoesNotExist:
            raise APIInputException(message='PlaylistMusic does not exist',
                                    response=Response(status=status.HTTP_404_NOT_FOUND,
                                                      data={'details': 'entry in playlist does not exist'}))
        except Playlist.DoesNotExist:
            raise APIInputException(message='Playlist does not exist',
                                    response=Response(status=status.HTTP_404_NOT_FOUND,
                                                      data={'details': 'playlist does not exist'}))

        if request.user.id != playlist.account_id:
            raise APIInputException(message='User is not the owner of the playlist',
                                    response=Response(status=status.HTTP_403_FORBIDDEN,
                                                      data={'details': 'not the owner of the playlist'}))
        return playlist_music, playlist

    @staticmethod
    def create(request):
        # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'details': 'dupa'})
        try:
            playlist = Playlist.objects.get(pk=request.data['playlist_id'])
            recording = Recording.objects.get(pk=request.data['recording_id'])
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'details': 'playlist does not exist.'})
        except Recording.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'details': 'recording does not exist.'})

        if playlist.account != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'not the owner of the playlist.'})

        music_count = get_playlist_music_count(playlist)
        playlist_music = {
            'playlist': playlist.id,
            'recording': recording.id,
            'playlist_position': music_count+1
        }
        print(playlist_music)

        serializer = PlaylistMusicSerializer(data=playlist_music)
        if serializer.is_valid():
            playlist.music_count += 1
            playlist.length += recording.length
            # TODO: transaction
            serializer.save()
            playlist.save()
            return Response(status=status.HTTP_201_CREATED, data={'details': 'recording added to the playlist.'})
        else:
            return Response(serializer.errors)

    @staticmethod
    def partial_update(request, pk):
        try:
            playlist_music, playlist = PlaylistMusicViewSet.get_playlist_music_data(request, pk)
        except APIInputException as e:
            return e.response

        old_position = playlist_music.playlist_position
        new_position = request.data['new_position']

        change = 1 if old_position > new_position else -1
        music_list = PlaylistMusic.objects.filter(playlist_id=playlist.id,
                                                  playlist_position__gte=min(old_position, new_position),
                                                  playlist_position__lte=max(old_position, new_position))

        with transaction.atomic():
            for music in music_list:
                music.playlist_position += change
                music.save()
            playlist_music.playlist_position = new_position
            playlist_music.save()

        return Response(status=status.HTTP_200_OK, data={'details': 'position changed.'})

    @staticmethod
    def delete(request, pk):
        try:
            playlist_music, playlist = PlaylistMusicViewSet.get_playlist_music_data(request, pk)
        except APIInputException as e:
            return e.response

        music_list = PlaylistMusic.objects.filter(playlist_id=playlist.id,
                                                  playlist_position__gt=playlist_music.playlist_position)
        with transaction.atomic():
            if len(music_list):
                for music in music_list:
                    music.playlist_position -= 1
                    music.save()
            playlist_music.delete()

        return Response(status=status.HTTP_200_OK, data={'details': 'removed from playlist.'})
