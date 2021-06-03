from django.urls import path, include
from rest_framework.routers import DefaultRouter

from uptime.views import DomainViewSet, CheckViewSet

router = DefaultRouter()
router.register("domains", DomainViewSet)
router.register("checks", CheckViewSet)
urlpatterns = router.urls

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]
print(*urlpatterns, sep="\n")
