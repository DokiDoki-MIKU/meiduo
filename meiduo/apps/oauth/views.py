from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from django.contrib.auth import login
from apps.oauth.models import OAuthQQUser
# Create your views here.
from django.http import JsonResponse
from meiduo import settings
class QQLoginURLView(View):
    def get(self,request):

        qq=OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_ClIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT,
            state='xxxxx'
        )
        qq_login_url=qq.get_qq_url()
        return JsonResponse({'code':0,'errmsg':'ok','login_url':qq_login_url})
class OauthQQView(View):
    def get(self,request):
        code=request.GET.get('code')
        if code is None:
            return JsonResponse({'code':400,'errmsg':'参数错误'})
        qq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_ClIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT,
            state='xxxxx'
        )
        token=qq.get_access_token(code)
        openid=qq.get_open_id(token)

        try:
            qquser=OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            from apps.oauth.utils import generic_openid
            access_token=generic_openid(openid)



            response = JsonResponse({'code':400,'access_token':access_token})
            return response

        else:
            login(request,qquser.user)
            response = JsonResponse({'code':0,'errmsg':'ok'})

            response.set_cookie('username',qquser.user.username)

from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login
from apps.users.models import User
import json
import re





class OautQQView(View):
    def get(self,request):...

    def post(self,request):
        data = json.loads(request.body.decode())

        mobile=data.get('mobile')
        password=data.get('password')
        sms_code=data.get('sms_code')
        access_token=data.get('access_token')

        from apps.oauth.utils import check_access_token
        openid=check_access_token(access_token)
        if openid is None:
            return JsonResponse({'coed':400,'errmsg':'参数缺失'})



        if not all([mobile, password, sms_code]):
            return JsonResponse({'code': 400,'errmsg': '缺少必传参数'})

            # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,'errmsg': '请输入正确的手机号码'})

            # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400,'errmsg': '请输入8-20位的密码'})

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:

            user=User.objects.create_user(username=mobile,mobile=mobile,password=password)

        else:
            if not user.check_password(password):
                return JsonResponse({'code':400,'errmsg':'账号或密码错误'})
        OAuthQQUser.objects.create(user=user,openid=openid)

        login(request,user)

        response=JsonResponse({'code':0,'errmsg':'ok'})
        response.set_cookie('username',user.username)
        return response
from meiduo import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
s=Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
token=s.dumps({'openid':'123456789'})

#b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwMjMzMTg4MiwiZXhwIjoxNjAyMzM1NDgyfQ.eyJvcGVuaWQiOiIxMjM0NTY3ODkifQ.k2ddFpUzXtkINL1tgfuIzJKcEyPjkz-DDlTyXZRqIliH9T0AinQ7iwGX9YVeVz_c3g1D37cYa0B2l0dfOwMMYA'

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
s=Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
s.loads(token)







































