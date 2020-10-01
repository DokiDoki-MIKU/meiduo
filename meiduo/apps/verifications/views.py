from django.shortcuts import render

from django.views import View
# Create your views here.
class HttpResonse(object):
    pass


class ImageCodeView(View):
    def get(self,request,uuid):
        from libs.captcha.captcha import captcha
        text,image = captcha.generate_captcha()
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid,100,text)
        return HttpResonse(image,content_type='image/jpeg')
        pass

