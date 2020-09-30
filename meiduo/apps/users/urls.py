from django.urls import path

from apps.users import views
from apps.users.views import UsernameCountView
urlpatterns = [
    path('usernames/<user>/count',UsernameCountView.as_view()),
    path('register/',views.RegisterView.as_view())
]