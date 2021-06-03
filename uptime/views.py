from django.utils.http import urlencode
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField
from rest_framework.viewsets import ModelViewSet

from uptime.models import Check, Domain


class DomainSerializer(HyperlinkedModelSerializer):
    checks_url = SerializerMethodField()

    class Meta:
        model = Domain
        fields = ["domain", "is_up", "checks_url", "url"]

    def get_checks_url(self, obj):
        path = reverse("check-list", request=self.context["request"])
        query = urlencode({"domain": obj.pk})
        return f"{path}?{query}"


class CheckSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsSafe(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class DomainViewSet(ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsOwner | IsSafe]  # type: ignore  # pylint: disable=E1131

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CheckViewSet(ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    filterset_fields = ["domain"]
