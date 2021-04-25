from django.urls import path
from uptime.views import DomainViewSet, CheckViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("domains", DomainViewSet)
router.register("checks", CheckViewSet)
urlpatterns = router.urls

print(*urlpatterns, sep="\n")
