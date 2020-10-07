from django.middleware import http
from django.shortcuts import render

# Create your views here
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
import re

# class UsernameCountView(View):
#     def get (self,request,username):
#         if not re.match('[a-zA-Z0-9_-]{5-20}',username):
#             return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})
#
#         count=User.objects.filter(username=username).count()
#         return JsonResponse({'code':0,'count':count,'errmsg':'ok'})
#         pass
class UsernameCountView(View):

    def get(self,request,username):
        # 1.  接收用户名，对这个用户名进行一下判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}',username):
        #     return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})
        # 2.  根据用户名查询数据库
        count=User.objects.filter(username=username).count()
        # 3.  返回响应
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})


import json


def user(args):
    pass


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



        from django.contrib.auth import login
        login(request,user)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})

class LoginView(View):
    def post(self,request):
        data=json.loads(request.body.decode())
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')

        if not all([username,password]):
            return JsonResponse({'code':400,'errmsg':'参数错误'})


        import re
        if re.match('^1[3-9]\d{9}$',username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'


        from django.contrib.auth import authenticate
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'账号或密码错误'})
        from django.contrib.auth import login
        login(request,user)
        if remembered is not None:
            request.session.set_expiry(None)


        else:
            request.session.set_expiry(0)


        return JsonResponse({'code':0,'errmsg':'ok'})