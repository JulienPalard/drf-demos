from django.urls import path
from file.views import file_view

urlpatterns = [
    path("<path:file>", file_view, name="file"),
    path("", file_view, name="file"),
]
