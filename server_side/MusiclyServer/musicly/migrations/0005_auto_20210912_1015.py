# Generated by Django 3.1.5 on 2021-09-12 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicly', '0004_auto_20210910_1820'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='usermusic',
            name='usermusic_listen_count_check',
        ),
        migrations.RemoveField(
            model_name='usermusic',
            name='listen_count',
        ),
    ]