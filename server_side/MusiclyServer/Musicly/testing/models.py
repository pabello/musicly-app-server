# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Recording(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recording'

class Artist(models.Model):
    id = models.BigAutoField(primary_key=True)
    stage_name = models.CharField(max_length=48)
    recordings = models.ManyToManyField(Recording)

    class Meta:
        managed = False
        db_table = 'artist'
