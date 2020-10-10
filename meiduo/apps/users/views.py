from django.middleware import http
from django.shortcuts import render

# Create your views here
from django.views import View
from django_redis import get_redis_connection

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

        sms_code_client = body_dict.get('sms_code')
        redis_conn = get_redis_connection('code')
        sms_code_server = redis_conn.get(mobile)
        if not sms_code_server:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        # 对比用户输入的和服务端存储的短信验证码是否一致
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})

        if not all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('[0-9A-Za-z]{8,20}',password):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[0-9A-Za-z]{8,20}',password2 ):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})
        if not re.match('1[3-9]\d{9}',mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        user=User.objects.create_user(username=username,password=password,mobile=mobile)



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

# class LoginView(View):
#
#     def post(self,request):
#         # 1. 接收数据
#         data=json.loads(request.body.decode())
#         username=data.get('username')
#         password=data.get('password')
#         remembered=data.get('remembered')
#         # 2. 验证数据
#         if not all([username,password]):
#             return JsonResponse({'code':400,'errmsg':'参数不全'})
#
#
#         # 确定 我们是根据手机号查询 还是 根据用户名查询
#
#         # USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
#         # 来影响authenticate 的查询
#         # authenticate 就是根据 USERNAME_FIELD 来查询
#         if re.match('1[3-9]\d{9}',username):
#             User.USERNAME_FIELD='mobile'
#         else:
#             User.USERNAME_FIELD='username'
#
#         # from django.contrib.auth import authenticate
#         # user=authenticate(username=username,password=password)
#         # if user is None:
#         #     return JsonResponse({'code':400,'errmsg':'账号或密码错误'})
#         from django.contrib.auth import login
#         login(request, user)
#         # 5. 判断是否记住登录
#         if remembered:
#             # 记住登录 -- 2周 或者 1个月 具体多长时间 产品说了算
#             request.session.set_expiry(None)
#
#         else:
#             # 不记住登录  浏览器关闭 session过期
#             request.session.set_expiry(0)
#
#         # 6. 返回响应
#         response = JsonResponse({'code': 0, 'errmsg': 'ok'})
#         # 为了首页显示用户信息
#         response.set_cookie('username', username)
#
#         return response
class LoginView(View):

    def post(self,request):
        # 1. 接收数据
        data=json.loads(request.body.decode())
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')
        # 2. 验证数据
        # if not all([username,password]):
        #     return JsonResponse({'code':400,'errmsg':'参数不全'})
        #
        #
        # # 确定 我们是根据手机号查询 还是 根据用户名查询
        #
        # # USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
        # # 来影响authenticate 的查询
        # # authenticate 就是根据 USERNAME_FIELD 来查询
        # if re.match('1[3-9]\d{9}',username):
        #     User.USERNAME_FIELD='mobile'
        # else:
        #     User.USERNAME_FIELD='username'

        # 3. 验证用户名和密码是否正确
        # 我们可以通过模型根据用户名来查询
        # User.objects.get(username=username)


        # 方式2
        from django.contrib.auth import authenticate
        # authenticate 传递用户名和密码
        # 如果用户名和密码正确，则返回 User信息
        # 如果用户名和密码不正确，则返回 None
        user=authenticate(username=username,password=password)

        if user is None:
            return JsonResponse({'code':400,'errmsg':'账号或密码错误'})

        # 4. session
        from django.contrib.auth import login
        login(request,user)
        # 5. 判断是否记住登录
        if remembered:
            # 记住登录 -- 2周 或者 1个月 具体多长时间 产品说了算
            request.session.set_expiry(None)

        else:
            #不记住登录  浏览器关闭 session过期
            request.session.set_expiry(0)

        # 6. 返回响应
        response = JsonResponse({'code':0,'errmsg':'ok'})
        # 为了首页显示用户信息
        response.set_cookie('username',username)

        return response

from django.contrib.auth import logout
class LogoutView(View):
    def delete(self,request):
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.delete_cookie('username')

        return response


from django.contrib.auth.mixins import LoginRequiredMixin
class CenterView(LoginRequiredMixin,View):
    def get(selfself,request):
        info_data = {
            'username':request.user.username,
            'email':request.user.email,
            'mobile':request.user.mobile,
            'email_active':request.user.email_active,


        }
        return JsonResponse({'code':0,'errmsg':'ok','info_data':info_data})

