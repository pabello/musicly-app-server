from django.urls import path, include
from .views_old import headers, json_input
from .views.music_view import ArtistViewSet, RecodingViewSet
from .views.account_view import AccountViewSet, register, change_password, create_reset_token, send_mail
from .views.playlist_view import PlaylistViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'artist', ArtistViewSet, 'artist')
router.register(r'recording', RecodingViewSet, 'recording')
router.register(r'account', AccountViewSet, 'account')
router.register(r'playlist', PlaylistViewSet, 'playlist')

urlpatterns = [
    path('testing/headers/', headers),  # delete this later
    path('testing/json/', json_input),  # delete this later
    path('register/', register, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('changePassword/', change_password, name='changePassword'),
    path('resetPassword/', create_reset_token, name='resetPassword'),
    path('sendMail/', send_mail, name='sendMail'),
    path('', include(router.urls))
]
