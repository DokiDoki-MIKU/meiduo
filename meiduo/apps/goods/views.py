from django.shortcuts import render


from fdfs_client.client import Fdfs_client

from apps.goods.models import GoodsCategory
from utils.goods import get_categories

client=Fdfs_client('utils/fastdfs/client.conf')

# client.upload_by_filename('/home/ubuntu/Desktop/01.jp
from django.views import View
from apps.contents.models import ContentCategory
class IndexView(View):

    def get(self,request):

        """
        首页的数据分为2部分
        1部分是 商品分类数据
        2部分是 广告数据

        """
        # 1.商品分类数据
        categories=get_categories()
        # 2.广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 我们的首页 后边会讲解页面静态化
        # 我们把数据 传递 给 模板
        context = {
            'categories': categories,
            'contents': contents,
        }
        # 模板使用比较少，以后大家到公司 自然就会了
        return render(request,'index.html',context)

from apps.goods.models import SKU
from django.http import JsonResponse
class ListView(View):
    def get(self,request,category_id):
        ordering=request.GET.get('ordering')
        page_size=request.GET.get('page_size')
        page=request.GET.get('page')
        try:
            category=GoodsCategory.objects.get(id=category_id)
        except GoodsCategory .DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'参数缺失'})

        breadcrumb=get_categories(category)
        skus=SKU.objects.filter(category=category,is_launched=True).order_by(ordering)
        from django.core.paginator import Paginator
        paginator=Paginator(skus,per_page=page_size)
        page_skus=paginator.page(page)
        sku_list=[]

        for sku in page_skus.object_list:
            sku_list.append({
                'id':sku.id,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price
            })

        total_num= paginator.num_pages

        return JsonResponse({'code':0,'errmsg':'OK','list':sku_list,'count':total_num,'breadcrumb':breadcrumb})


from haystack.views import SearchView
from django.http import JsonResponse


class SKUSearchchView(SearchView):
    def create_response(self):
        context = self.get_context()

        sku_list=[]
        for item in context['page'].object_list:
            sku_list.append({
                'id':item.object.id,
                'name':item.object.name,
                'price': item.object.price,
                'default_image_url': item.object.default_image.url,
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })

        return JsonResponse(sku_list,safe=False)
from utils.goods import get_categories,get_breadcrumb,get_goods_specs
class DetailView(View):
    def get(self,request,sku_id):
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            pass
        categories=get_categories()
        breadcrumb=get_breadcrumb(sku.category)
        goods_specs=get_goods_specs(sku)
        context={
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs':goods_specs,
        }

        return render(request,'detail.html',context)




