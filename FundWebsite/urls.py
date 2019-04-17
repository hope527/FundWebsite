from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from fundapp.views import index, index_response, test, test_respoonse, search, index_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('index/p=<int:page>', index_response),
    path('index/c=<str:column>&key=<str:keyword>', search),
    path('index/id=<str:fund_id>&area=<str:area>', index_form),
    path('test/', test),
    path('test/<slug:start>&<slug:end>&<str:investement_type>&<str:ratio>&<int:btest_time>&<int:money>&<str:buy_ratio>&<int:strategy>&<int:frequency>/', test_respoonse),
]
