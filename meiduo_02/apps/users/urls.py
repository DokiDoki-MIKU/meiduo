from django.urls import path
from apps.users.views import UsernameCountView
urlpatterns = [
    path('username/<username>/count',UsernameCountView.as_view())

]