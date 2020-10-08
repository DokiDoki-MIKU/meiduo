from django.urls import path
from apps.oauth.views import QQLoginURLView

urlpatterns = [
    path('image_codes/<uuid>/',QQLoginURLView.as_view()),
]