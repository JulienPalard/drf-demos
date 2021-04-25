from django.urls import path, include
from uptime.views import DomainViewSet, CheckViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("domains", DomainViewSet)
router.register("checks", CheckViewSet)
urlpatterns = router.urls

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]
print(*urlpatterns, sep="\n")
