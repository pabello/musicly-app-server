from django.urls import path, include
from .views.music_view import ArtistViewSet, RecodingViewSet
from .views.account_view import register, change_password, create_reset_token, account_details, delete_account, \
    confirm_email, resend_confirmation_mail
from .views.playlist_view import PlaylistViewSet, PlaylistMusicViewSet
from .views.user_music_view import user_music_list, add_music_reaction
from .views.recommendations_view import recommendation_list, next_recommendation
from rest_framework.routers import DefaultRouter
from .views.auth import obtain_auth_token

router = DefaultRouter()
router.register(r'artist', ArtistViewSet, 'artist')
router.register(r'recording', RecodingViewSet, 'recording')
router.register(r'playlist', PlaylistViewSet, 'playlist')
router.register(r'playlistMusic', PlaylistMusicViewSet, 'playlistMusic')

urlpatterns = [
    path('account/', account_details, name='accountDetails'),
    path('account/delete/', delete_account, name='deleteAccount'),
    path('register/', register, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('changePassword/', change_password, name='changePassword'),
    path('resetPassword/', create_reset_token, name='resetPassword'),
    path('confirmationMail/', resend_confirmation_mail, name='confirmationMail'),
    path('confirmEmail/<int:pk>/<str:token>/', confirm_email, name='confirmEmail'),
    path('userMusic/', user_music_list, name='userMusic'),
    path('userMusic/<int:pk>/', add_music_reaction, name='musicReaction'),
    path('recommendations/', recommendation_list, name='recommendationList'),
    path('recommendation/', next_recommendation, name='nextRecommendation'),
    path('', include(router.urls))
]
