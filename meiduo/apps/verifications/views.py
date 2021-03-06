from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
# Create your views here.
# class HttpResponse(object):
#     pass


class ImageCodeView(View):

    def get(self,request,uuid):

        from libs.captcha.captcha import captcha
        text,image = captcha.generate_captcha()

        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid,100,text)

        return HttpResponse(image,content_type='image/jpeg')


class SmsCodeView(View):
    def get(self,request,mobile):
        image_code=request.GET.get('image_code')
        uuid=request.GET.get('image_code_id')

        if not all([image_code,uuid]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})

        from django_redis import get_redis_connection
        redis_cli=get_redis_connection('code')
        redis_image_code=redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code':400,'errmsg':'图形验证码已过期'})

        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code':400,'errmsg':'验证码错误'})

        send_flag = redis_cli.get('send_flag_%s'%mobile)
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})


        from random import randint
        sms_code='%06d'%randint(0,999999)
        # sms_code=77777
        pipeline=redis_cli.pipeline()

        redis_cli.setex(mobile,300,sms_code)
        redis_cli.setex('send_flag_%s'%mobile,60,1)

        pipeline.execute()

        # from libs.yuntongxun.sms import CCP
        # CCP().send_template_sms(mobile,[sms_code,5],1)

        from celery_tasks.sms.tasks import celery_send_sms_code
        celery_send_sms_code.delay(mobile,sms_code)
        return JsonResponse({'code':0,'errmsg':'ok'})

