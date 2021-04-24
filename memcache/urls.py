from django.urls import path
from memcache.views import root, cache


urlpatterns = [path("", root), path("<str:key>", cache)]
