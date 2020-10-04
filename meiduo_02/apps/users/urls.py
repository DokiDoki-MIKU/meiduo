from django.urls import path
from apps.users.views import UsernameCountView,RegisterView
from . import views
urlpatterns = [
    path('username/<username:username>/count',UsernameCountView.as_view()),
    path('register/',RegisterView.as_view()),
    path('usernames/<username:username>/count/',views.UsernameCountView.as_view()),

]