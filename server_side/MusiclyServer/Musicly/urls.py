from django.urls import path, include
from .views_old import headers, json_input
from .views.music_view import ArtistViewSet, RecodingViewSet
from .views.account_view import AccountViewSet
from .views.playlist_view import PlaylistViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'artist', ArtistViewSet, 'artist')
router.register(r'recording', RecodingViewSet, 'recording')
router.register(r'account', AccountViewSet, 'account')
router.register(r'playlist', PlaylistViewSet, 'playlist')

urlpatterns = [
    path('testing/headers/', headers),  # delete this later
    path('testing/json/', json_input),  # delete this later
    path('', include(router.urls))
]
