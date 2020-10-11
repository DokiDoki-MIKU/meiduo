from django.urls import path
from apps.oauth.views import QQLoginURLView,OauthQQView

urlpatterns = [
    path('image_codes/<uuid>/',QQLoginURLView.as_view()),
    path('oauth_callback/<uuid>/',OauthQQView.as_view()),
]