from django.contrib import admin
from .models import Account, Artist, PasswordResetToken, Performed, Playlist, PlaylistMusic, Recording, UserMusic

# Register your models here.
admin.site.register(Account)
admin.site.register(Artist)
admin.site.register(PasswordResetToken)
admin.site.register(Performed)
admin.site.register(Playlist)
admin.site.register(PlaylistMusic)
admin.site.register(Recording)
admin.site.register(UserMusic)