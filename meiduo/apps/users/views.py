from django.middleware import http
from django.shortcuts import render

# Create your views here
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
import re

class UsernameCountView(View):
    def get (self,request,username):
        if not re.match('[a-zA-Z0-9_-]{5-20}',username):
            return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})

        count=User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})
        pass

class RegisterView(View):
    def post(self,request):

        pass

import json
class RegisterView(View):
    def post(self,request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)

        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        if not all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('[a-zA-Z_-]{5,20}'):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[0-9A-Za-z]{8,20}',password ):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('1[3-9]\d{9}',mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        User.objects.create(username=username,password=password,mobile=mobile)

        return JsonResponse({'code':0,'errmsg':'ok'})