from django.urls import path
from apps.goods.views import IndexView,ListView
from apps.goods.views import SKUSearchchView,DetailView
urlpatterns = [
    path('index/',IndexView.as_view()),
    path('list/<category_id>/skus/',ListView.as_view()),
    path('search/',SKUSearchchView()),
    path('detail/<sku_id>/',DetailView()),
]

