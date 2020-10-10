from django.urls import path
from . import views
from apps.users import views
from apps.users.views import UsernameCountView, RegisterView, MobileCountView,LoginView,LogoutView
from apps.users.views import CenterView
urlpatterns = [
    # path('usernames/<user>/count/',UsernameCountView.as_view()),
    path('usernames/<username>/count/',UsernameCountView.as_view()),
    path('register/',RegisterView.as_view()),
    path('mobiles/<mobile>/count/',MobileCountView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('center/',LogoutView.as_view())

]