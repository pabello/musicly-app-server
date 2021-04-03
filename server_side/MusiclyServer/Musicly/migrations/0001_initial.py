# Generated by Django 3.1.5 on 2021-03-20 23:38

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('stage_name', models.CharField(max_length=400)),
            ],
            options={
                'db_table': 'musicly_artist',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Performed',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'musicly_performed',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=2000)),
                ('length', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'musicly_recording',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('length', models.IntegerField(default=0, verbose_name='Total playtime of the playlist playlist')),
                ('music_count', models.IntegerField(default=0, verbose_name='Number of recordings in the playlist')),
            ],
            options={
                'db_table': 'musicly_playlist',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserMusic',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('like_status', models.IntegerField(choices=[(-1, 'dislike'), (0, 'neutral'), (1, 'like')], default=0)),
                ('listen_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'musicly_user_music',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='unique username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=128, verbose_name='hashed password')),
                ('is_active', models.BooleanField(default=True, verbose_name='account active')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login time')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email_confirmed', models.BooleanField(default=False, verbose_name='email confirmed')),
                ('music', models.ManyToManyField(through='Musicly.UserMusic', to='Musicly.Recording')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'musicly_account',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Musicly.account')),
                ('token', models.CharField(max_length=64, unique=True, validators=[django.core.validators.RegexValidator(code='no_match', message='Length has to be 64', regex='^.{64}$')])),
                ('expires_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'musicly_password_reset_token',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='usermusic',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermusic',
            name='recording',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musicly.recording'),
        ),
        migrations.CreateModel(
            name='PlaylistMusic',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('playlist_position', models.IntegerField(default=0, verbose_name='Position in playlist')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musicly.playlist')),
                ('recording', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Musicly.recording')),
            ],
            options={
                'db_table': 'musicly_playlist_music',
                'ordering': ['playlist_position'],
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='recordings',
            field=models.ManyToManyField(related_name='belong_to_playlist', through='Musicly.PlaylistMusic', to='Musicly.Recording'),
        ),
        migrations.AddConstraint(
            model_name='usermusic',
            constraint=models.CheckConstraint(check=models.Q(listen_count__gte=0), name='usermusic_listen_count_check'),
        ),
        migrations.AlterUniqueTogether(
            name='usermusic',
            unique_together={('account', 'recording')},
        ),
        migrations.AddConstraint(
            model_name='playlistmusic',
            constraint=models.CheckConstraint(check=models.Q(playlist_position__gte=0), name='playlist_music_position_check'),
        ),
        migrations.AlterUniqueTogether(
            name='playlistmusic',
            unique_together={('playlist', 'playlist_position')},
        ),
        migrations.AddConstraint(
            model_name='playlist',
            constraint=models.CheckConstraint(check=models.Q(length__gte=0), name='playlist_length_check'),
        ),
        migrations.AddConstraint(
            model_name='playlist',
            constraint=models.CheckConstraint(check=models.Q(music_count__gte=0), name='playlist_music_count_check'),
        ),
        migrations.AlterUniqueTogether(
            name='playlist',
            unique_together={('account', 'name')},
        ),
    ]
