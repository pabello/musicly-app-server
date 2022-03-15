# Generated by Django 3.1.5 on 2021-08-23 12:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('musicly', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='modification_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Latest playlist change time'),
        ),
        migrations.AlterField(
            model_name='usermusic',
            name='status_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Latest status change time'),
        ),
    ]
