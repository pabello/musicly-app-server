# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.timezone import now


class Artist(models.Model):
    id = models.BigAutoField(primary_key=True)
    stage_name = models.CharField(max_length=400)
    recordings = models.ManyToManyField('Recording', related_name='artists_list', through='Performed')

    class Meta:
        managed = False
        db_table = 'musicly_artist'

    def __str__(self):
        return self.stage_name


class Recording(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=2000)
    length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'musicly_recording'

    def __str__(self):
        data = {"id": self.id, "title": self.title}
        return data.__str__()


class Performed(models.Model):
    id = models.BigAutoField(primary_key=True)
    recording = models.ForeignKey(Recording, models.RESTRICT)
    artist = models.ForeignKey(Artist, models.RESTRICT)

    class Meta:
        managed = False
        db_table = 'musicly_performed'
        unique_together = ('recording', 'artist')

    def __str__(self):
        return f'{self.artist} performed {self.recording}'


# class User(AbstractUser):
#     pass


class Account(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=32, verbose_name='unique username')
    email = models.CharField(unique=True, max_length=254, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='hashed password')
    is_active = models.BooleanField(default=True, verbose_name='account active')
    last_login = models.DateTimeField(default=now, verbose_name='last login time')
    date_joined = models.DateTimeField(default=now, verbose_name='date joined')
    email_confirmed = models.BooleanField(default=False, verbose_name='email confirmed')

    music = models.ManyToManyField(Recording, through='UserMusic')

    is_superuser = None
    first_name = None
    last_name = None
    is_staff = None
    groups = None

    class Meta:
        managed = True
        db_table = 'musicly_account'

    def __str__(self):
        return f'({self.id}) {self.username}'


class PasswordResetToken(models.Model):
    account = models.OneToOneField(Account, models.CASCADE, primary_key=True)
    token = models.CharField(unique=True, max_length=64, validators=[RegexValidator(regex='^.{64}$',
                                                                                    message='Length has to be 64',
                                                                                    code='no_match')])
    expires_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'musicly_password_reset_token'

    def __str__(self):
        return f'token for user {self.account}'


class Playlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, models.CASCADE)
    name = models.CharField(max_length=64, blank=False, null=False)
    length = models.IntegerField(default=0, verbose_name='Total playtime of the playlist playlist')
    music_count = models.IntegerField(default=0, verbose_name='Number of recordings in the playlist')

    recordings = models.ManyToManyField(Recording, related_name='belong_to_playlist', through='PlaylistMusic')

    class Meta:
        managed = True
        db_table = 'musicly_playlist'
        unique_together = ('account', 'name')

    def __str__(self):
        return self.name


class PlaylistMusic(models.Model):
    id = models.BigAutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, models.CASCADE)
    recording = models.ForeignKey(Recording, models.CASCADE)
    playlist_position = models.IntegerField('Position in playlist')

    class Meta:
        managed = True
        db_table = 'musicly_playlist_music'
        unique_together = ('playlist', 'playlist_position')
        ordering = ['playlist_position']  # Might require unique set (playlist, position) as position is not unique

    def __str__(self):
        return f'({self.id}) {self.recording} in playlist {self.playlist} on position {self.playlist_position}'


class UserMusic(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, models.CASCADE)
    recording = models.ForeignKey(Recording, models.CASCADE)
    like_status = models.IntegerField()
    listen_count = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'musicly_user_music'
        unique_together = ('account', 'recording')

    def __str__(self):
        return f'{self.recording} listened by user {self.account}'
