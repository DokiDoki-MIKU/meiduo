from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from django.core.cache import cache
from django_redis.serializers import json

from apps.areas.models import Area
from utils.views import LoginRequiredJSONMixin


class AreaView(View):

    def get(self,request):

        # 先查询缓存数据
        province_list=cache.get('province')
        # 如果没有缓存，则查询数据库，并缓存数据
        if province_list is None:
            # 1.查询省份信息
            provinces=Area.objects.filter(parent=None)
            # 查询结果集

            # 2.将对象转换为字典数据
            province_list = []
            for province in provinces:
                province_list.append({
                    'id':province.id,
                    'name':province.name
                })

            # 保存缓存数据
            # cache.set(key,value,expire)
            cache.set('province',province_list,24*3600)
        # 3.返回响应
        return JsonResponse({'code':0,'errmsg':'ok','province_list':province_list})


class SubAreaView(View):

    def get(self,request,id):

        # 先获取缓存数据
        data_list=cache.get('city:%s'%id)

        if data_list is None:
            # 1.获取省份id、市的id,查询信息
            # Area.objects.filter(parent_id=id)
            # Area.objects.filter(parent=id)

            up_level = Area.objects.get(id=id)  #
            down_level=up_level.subs.all()  #
            # 2.将对象转换为字典数据
            data_list=[]
            for item in down_level:
                data_list.append({
                    'id':item.id,
                    'name':item.name
                })

            #缓存数据
            cache.set('city:%s'%id,data_list,24*3600)

        # 3.返回响应
        return JsonResponse({'code':0,'errmsg':'ok','sub_data':{'subs':data_list}})




