import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
import pickle
import base64

class CartView(View):
    def post(self,request):
        data=json.loads(request.body.decode())
        sku_id=data.get('sku_id')
        count=data.get('count')

        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'查无此商品'})

        try:
            count=int(count)
        except SKU.DoesNotExist:
            count = 1

        user=request.user
        if user.is_authenticated:
            redis_cli=get_redis_connection('carts')
            pipline=redis_cli.pipline()
            pipline.hincrby('carts_%s'%user.id,sku_id,count)
            pipline.sadd('selected_%s'%user.id,sku_id)

            pipline.execute()

            return JsonResponse({'code':0,'errmsg':'ok'})
        else:
            cookie_carts=request.COOKIES.get('cats')

            if cookie_carts:
                carts = pickle.loads(base64.b64decode(cookie_carts))

            else:
                carts={}

            if sku_id in carts:
                origin_count = carts[sku_id]['count']
                count += origin_count

                carts[sku_id]={
                    'count':count,
                    'select':True
                }

            carts_bytes=pickle.dumps(carts)
            base64encode=base64.b64encode(carts_bytes)
            response = JsonResponse({'code':0,'errmsg':'ok'})
            response.set_cookie('carts',base64encode.decode(),max_age=3600*24*12)
            return response

    def get(self,request):
        user=request.user
        if user.is_authenticated:
            redis_cil=get_redis_connection('carts')
            sku_id_counts=redis_cil.hgethall('carts_%s'%user.id)
            selected_ids=redis_cil.smembers('selectes_%s'%user.id)
            carts={}

            for sku_id,count in sku_id_counts.items():
                carts[int(sku_id)]={
                    'count':int(count),
                    'selected':sku_id in selected_ids
                }

        else:
            cookie_carts=request.COOKIES.get('carts')

            if cookie_carts is not None:
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                carts={}

            sku_ids=carts.keys()
            skus=SKU.objects.filter(id__in=sku_ids)

            sku_list=[]
            for sku in skus:
                sku_list.append({
                    'id': sku.id,
                    'price': sku.price,
                    'name': sku.name,
                    'default_image_url': sku.default_image.url,
                    'selected': carts[sku.id]['selected'],  # 选中状态
                    'count': int(carts[sku.id]['count']),  # 数量 强制转换一下
                    'amount': sku.price * carts[sku.id]['count']  # 总价格
                }
                )
            return JsonResponse({'code':0,'errmsg':'ok','cart_sku':sku_list})
    def put(self,request):
        user=request.user
        data=json.loads(request.body.decode())
        sku_id=data.get('sku_id')
        count=data.get('count')
        selected=data.get('selected')

        if not  all([sku_id,count]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})

        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'没有此商品'})

        try:
            count=int(count)
        except Exception:
            count = 1

        if user.is_authenticated:
            redis_cli=get_redis_connection('carts')

            redis_cli.hset('carts_%s'%user.id,sku_id,count)
            if selected:
                redis_cli.sadd('selected_%s'%user.id,sku_id)

            return JsonResponse({'code':0,'errmsg':'ok','cart_sku':{'count':count,'selected':selected}})

        else:
            cookies_cart = request.COOKIES.get('carts')
            if cookies_cart is not None:
                carts=pickle.loads(base64.b64decode(cookies_cart))
            else:
                carts={}

            if sku_id in carts:
                carts[sku_id]={
                    'count':count,
                    'select':selected
                }
        new_carts=base64.b64encode(pickle.dumps(carts))
        response = JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_sku': {'count': count, 'selected': selected}})
        response.set_cookie('carts', new_carts.decode(), max_age=14 * 24 * 3600)
        return response

    def delete(self,request):
        data=json.loads(request.body.decode)
        sku_id=data.get('sku_id')
        try:
            SKU.objects.get(pk=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'没有此商品'})

        user=request.user
        if user.is_authenticated:
            redis_cli=get_redis_connection('carts')

            redis_cli.hdel('carts_%s'%user.id,sku_id)
            redis_cli.srem('select_%s'%user.id,sku_id)
            return JsonResponse({'code':0,'errmsg':'ok'})

        else:
            carts={}

        del carts[sku_id]
        new_carts=base64.b64encode(pickle.dumps(carts))
        response=JsonResponse({'code':0,'errmsg':'ok'})
        response.set_cookie('carts',new_carts.decode(),max_age=3600*24*14)
        return response


