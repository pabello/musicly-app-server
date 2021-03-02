# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import RegexValidator


class Artist(models.Model):
    id = models.BigAutoField(primary_key=True)
    stage_name = models.CharField(max_length=400)
    recordings = models.ManyToManyField('Recording', related_name='artists_list', through='Performed')

    class Meta:
        managed = False
        db_table = 'artist'

    def __str__(self):
        return self.stage_name


class Recording(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=2000)
    length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recording'

    def __str__(self):
        data = {"id": self.id, "title": self.title}
        return data.__str__()


class Performed(models.Model):
    id = models.BigAutoField(primary_key=True)
    recording = models.ForeignKey(Recording, models.RESTRICT)
    artist = models.ForeignKey(Artist, models.RESTRICT)

    class Meta:
        managed = False
        db_table = 'performed'
        unique_together = ('recording', 'artist')

    def __str__(self):
        return f'{self.artist} performed {self.recording}'


class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=32)
    email = models.CharField(unique=True, max_length=254)
    password_hash = models.CharField(max_length=64)
    confirmed = models.BooleanField()
    last_login_time = models.DateTimeField()

    music = models.ManyToManyField(Recording, through='UserMusic')

    class Meta:
        managed = False
        db_table = 'account'

    def __str__(self):
        return f'({self.id}) {self.username}'


class PasswordResetToken(models.Model):
    account = models.OneToOneField(Account, models.CASCADE, primary_key=True)
    token = models.CharField(unique=True, max_length=64, validators=[RegexValidator(regex='^.{64}$',
                                                                                    message='Length has to be 64',
                                                                                    code='no_match')])
    expires_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'password_reset_token'

    def __str__(self):
        return f'token for user {self.account}'


class Playlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, models.CASCADE)
    name = models.CharField(max_length=64, blank=True)
    length = models.IntegerField('Total playtime of the playlist playlist')
    music_count = models.IntegerField('Number of recordings in the playlist')

    recording = models.ManyToManyField(Recording, related_name='belong_to_playlist', through='PlaylistMusic')

    class Meta:
        managed = False
        db_table = 'playlist'

    def __str__(self):
        return self.name


class PlaylistMusic(models.Model):
    id = models.BigAutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, models.CASCADE)
    recording = models.ForeignKey(Recording, models.CASCADE)
    playlist_position = models.IntegerField('Position in playlist')

    class Meta:
        managed = False
        db_table = 'playlist_music'
        unique_together = ('playlist', 'playlist_position')

    def __str__(self):
        return f'{self.recording} in playlist {self.playlist}'


class UserMusic(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, models.CASCADE)
    recording = models.ForeignKey(Recording, models.CASCADE)
    like_status = models.IntegerField()
    listen_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_music'
        unique_together = ('account', 'recording')

    def __str__(self):
        return f'{self.recording} listened by user {self.account}'
