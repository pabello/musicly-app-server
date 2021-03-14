from rest_framework import serializers
from .models import Artist, Account, Recording, Playlist, PlaylistMusic, UserMusic


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'stage_name']


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ['id', 'title', 'length']


class RecordingTitleSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField

    class Meta:
        model = Recording
        fields = ['title']


class ArtistDetailsSerializer(serializers.ModelSerializer):
    recordings = RecordingSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ['id', 'stage_name', 'recordings']


class RecordingDetailsSerializer(serializers.ModelSerializer):
    artists_list = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Recording
        fields = ['id', 'title', 'length', 'artists_list']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username']


class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'is_active', 'last_login']


class AccountLifecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password', 'is_active']


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'account', 'name', 'length', 'music_count']


class PlaylistMusicListSerializer(serializers.ModelSerializer):
    recordings = RecordingSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'account', 'name', 'length', 'music_count', 'recordings']


class PlaylistMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistMusic
        fields = ['id', 'playlist', 'recording', 'playlist_position']


class UserMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMusic
        fields = ['id', 'recording_id', 'like_status', 'listen_count']
