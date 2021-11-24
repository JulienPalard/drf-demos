from django.urls import path, include
from rest_framework import routers
from habitstracker import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("habits", views.HabitsViewSet, basename="habits")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
