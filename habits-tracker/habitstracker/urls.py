from django.urls import path, include
from habitstracker import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("habits", views.HabitsViewSet, basename="habits")

habits_router = routers.NestedSimpleRouter(
    parent_router=router, parent_prefix="habits", lookup="habit"
)
habits_router.register("done", views.DoneViewSet, basename="habits-done")


print(*router.urls, sep="\n")
print(*habits_router.urls, sep="\n")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(habits_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
