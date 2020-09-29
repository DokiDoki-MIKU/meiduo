from django.urls import path
from apps.users.views import UsernameCountView
urlpatterns = [
    path('usernames/<user>/count',UsernameCountView.as_view()),
]