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
            response = JsonResponse({'code':400,'access_token':openid})
            return response

        else:
            login(request,qquser.user)
            response = JsonResponse({'code':0,'errmsg':'ok'})

            response.set_cookie('username',qquser.user.username)


            pass













































