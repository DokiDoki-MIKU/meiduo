from django.shortcuts import render


from fdfs_client.client import Fdfs_client


from utils.goods import get_categories

client=Fdfs_client('utils/fastdfs/client.conf')

# client.upload_by_filename('/home/ubuntu/Desktop/01.jp
from django.views import View
from apps.contents.models import ContentCategory
class IndexView(View):

    def get(self,request):

        categories=get_categories()

        contents= {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories':categories,
            'contents':contents
        }

        return render(request,'index.html',context)