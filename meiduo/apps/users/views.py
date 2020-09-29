from django.shortcuts import render

# Create your views here
from django.views import View
from apps.users.models import User
from django.http import JsonResponse


class UsernameCountView(View):
    def get (self,requset,username):
        count=User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})
        pass