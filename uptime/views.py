from django.utils.http import urlencode
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from uptime.models import Domain, Check


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


class DomainViewSet(ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CheckViewSet(ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    filterset_fields = ["domain"]
