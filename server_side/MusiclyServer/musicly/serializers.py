from rest_framework import serializers
from .models import Artist, Account, Recording, Playlist, PlaylistMusic, UserMusic
from collections import OrderedDict


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


class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'is_active', 'email_confirmed', 'last_login']


class AccountLifecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password', 'is_active', 'email_confirmed']


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'account', 'name', 'length', 'music_count', 'modification_timestamp']


class PlaylistMusicListSerializer(serializers.ModelSerializer):
    recordings = RecordingSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'account', 'name', 'length', 'music_count', 'modification_timestamp', 'recordings']

    @staticmethod
    def get_recordings_list(instance: Playlist):
        ret = list()
        playlist_music = instance.recordings.through.objects.filter(playlist=instance)
        for record in playlist_music:
            data = OrderedDict()
            data['association_id'] = record.id
            data['recording_id'] = record.recording_id
            data['title'] = record.recording.title
            data['length'] = record.recording.length
            ret.append(data)
        return ret

    def to_representation(self, instance: Playlist):
        """Convert `username` to lowercase."""
        ret = OrderedDict()
        ret['id'] = instance.id
        ret['account'] = instance.account.id
        ret['name'] = instance.name
        ret['length'] = instance.length
        ret['music_count'] = instance.music_count
        ret['modification_timestamp'] = instance.modification_timestamp
        ret['recordings'] = self.get_recordings_list(instance)
        return ret


class PlaylistMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistMusic
        fields = ['id', 'playlist', 'recording', 'playlist_position']


class UserMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMusic
        fields = ['id', 'recording_id', 'like_status', 'status_timestamp']


class UserMusicRecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMusic
        fields = ['account_id', 'recording_id', 'like_status']


class UserMusicIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMusic
        fields = ['recording_id']
