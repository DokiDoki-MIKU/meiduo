from apps.contents.models import ContentCategory
from utils.goods import get_categories
import time

def generic_meiduo_index():
    print('--------------%s-------------' % time.ctime())
    categories = get_categories()
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

    from django.template import loader
    index_template = loader.get_template('index.html')

    index_html_data = index_template.render(context)
    from meiduo import settings
    import os

    file_path = os.path.join(os.path.dirname(settings.BASE_DIR, 'front_end_pc/index.html'))

    with open(file_path, 'w', encoding='utf-8')as f:
        f.write(index_html_data)




