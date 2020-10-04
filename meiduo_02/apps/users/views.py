import json

from django.shortcuts import render
from django.views import View
# Create your views here.
import re
from django.http import JsonResponse, HttpResponse
from apps.users.models import User
class UsernameCountView(View):

    def get(self,request,username):
        # if not re.match('[a-zA-Z0-9_-]{5,20}',username):
        #     return JsonResponse({'code':200,'errmsg':'用户名错误'})
        count=User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})

class RegisterView(View):
    def post(self,request):
        body_bytes=request.body
        body_str=body_bytes.decode()
        body_dict=json.loads(body_str)

        username=body_dict.get('username')
        password=body_dict.get('password')
        password2=body_dict.get('password2')
        mobile=body_dict.get('mobile')
        allow=body_dict.get('allow')

        if all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})

        if not re.match('[a-zA-Z]{5,20}',username):
            return JsonResponse({'code':400,'errmsg':'用户名不满足规则'})

        if re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code':400,'errmsg':'密码格式错误'})

        if password != password2:
            return JsonResponse({'code':400,'errmsg':'两次密码不正确'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})

        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})

        user=User.objects.create_user(username=username,password=password,mobile=mobile)
        # request.session['user_id']=user.id
        from django.contrib.auth import login
        login(request,user)

        return JsonResponse({'code':0,'errmsg':'ok!'})

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















