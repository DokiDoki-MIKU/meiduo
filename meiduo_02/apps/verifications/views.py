from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

class ImageCodeView(View):
    def get(selfself,request,uuid):
        from libs.captcha.captcha import captcha
        text,image=captcha.generate_captcha()

        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')

        redis_cli.setex(uuid,100,text)

        return HttpResponse(image,content_type='image/jpeg')
class SmscCodeView(View):
    def get(self,request,mobile):
        image_code=request.GET.get('image_code')
        uuid=request.GET.get('image_code_id')

        if not all([image_code,uuid]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})

        from  django_redis import get_redis_connection
        redis_cli=get_redis_connection('code')

        redis_image_code=redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code':400,'errmsg':'验证码已过期'})
        if redis_image_code != image_code:
            return JsonResponse({'code':400,'errmsg':'图片验证码错误'})
        from random import randint
        sms_code='%06d'%randint(0,999999)
        redis_cli.setex(mobile,300,sms_code)
        from libs.yuntongxun.sms import CCP
        CCP().send_template_sms(mobile,[sms_code,5],1)

        return  JsonResponse({'code':0,'errmsg':'ok!'})