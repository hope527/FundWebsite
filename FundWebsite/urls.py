from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from fundapp.views import home, mds, test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    url(r'^test/(?P<start>\d{4}-\d{2}-\d{2}) (?P<end>\d{4}-\d{2}-\d{2})/$', test),
    url(r'^ajax_list/(?P<start>\d{4}-\d{2}-\d{2}) (?P<time>\d{4}-\d{2}-\d{2})/$', mds),
]
