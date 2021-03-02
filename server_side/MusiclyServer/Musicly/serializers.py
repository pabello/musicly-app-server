from rest_framework import serializers
from .models import Artist, Account, Recording, Playlist, PlaylistMusic


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'stage_name']


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ['id', 'title', 'length']


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
        fields = ['id', 'username', 'email', 'confirmed', 'last_login_time']


class AccountLifecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password_hash', 'confirmed', 'last_login_time']


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'account_id', 'name', 'length', 'music_count']


class PlaylistMusicSerializer(serializers.ModelSerializer):
    recordings = RecordingSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'account_id', 'name', 'length', 'music_count', 'recordings']
