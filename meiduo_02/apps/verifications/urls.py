from django.urls import path
from apps.verifications.views import ImageCodeView

urlpatterns=[
    path('image_code/<uuid>/',ImageCodeView.as_view())
]