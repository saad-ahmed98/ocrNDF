from django.urls import re_path

from . import views  # import views so we can use them in urls.

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^ocr/$', views.easyOCR, name='ocr'),
]
