from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from fundapp.views import home, mds, test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    url(r'^test/(\w+)/$', test),
    url(r'^ajax_list/(\w+)/$', mds),
]
