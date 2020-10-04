from django.urls import path
from apps.users.views import UsernameCountView,RegisterView
urlpatterns = [
    path('username/<username:username>/count',UsernameCountView.as_view()),
    path('register/',RegisterView.as_view()),


]