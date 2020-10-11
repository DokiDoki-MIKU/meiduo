from django.urls import path
from apps.users.views import UsernameCountView,RegisterView,LoginView,LogoutView,EmailView
from apps.users.views import CenterView
urlpatterns = [
    #判断用户名是否重复
    path('usernames/<username:username>/count/',UsernameCountView.as_view()),
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('info/',CenterView.as_view()),
    path('emails/',EmailView.as_view()),
    # path('emails/verification/',EmailVerifyView.as_view()),

]