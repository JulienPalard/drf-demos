from django.urls import path
from uptime.views import uptime, uptimes, checks

urlpatterns = [
    path("", uptimes, name="domain-list"),
    path("<str:domain>", uptime, name="domain-detail"),
    path("<str:domain>/checks", checks, name="domain-checks"),
]
