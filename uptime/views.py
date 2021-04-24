from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
)
from rest_framework.response import Response
from uptime.models import Domain, Check


class DomainSerializer(HyperlinkedModelSerializer):
    checks = HyperlinkedIdentityField(view_name="domain-checks", lookup_field="domain")

    class Meta:
        model = Domain
        fields = "__all__"
        extra_kwargs = {
            "url": {"lookup_field": "domain"},
        }


class CheckSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Check
        exclude = ("domain", "url")


@api_view(["GET", "POST"])
def uptimes(request):
    if request.method == "POST":
        domain = DomainSerializer(data=request.data, context={"request": request})
        if not domain.is_valid():
            return Response(serializer.errors, status=400)
        domain.save()
        return Response(
            status=201,
            headers={
                "Location": reverse("domain-detail", args=(domain.data["domain"],))
            },
        )
    if request.method == "GET":
        return Response(
            DomainSerializer(
                Domain.objects.all(), many=True, context={"request": request}
            ).data
        )


@api_view(["GET", "DELETE"])
def uptime(request, domain):
    if request.method == "GET":
        return Response(
            DomainSerializer(
                Domain.objects.get(domain=domain), context={"request": request}
            ).data
        )
    if request.method == "DELETE":
        Domain.objects.get(domain=domain).delete()
        return Response(status=200)


@api_view(["GET"])
def checks(request, domain):
    return Response(
        CheckSerializer(
            Check.objects.filter(domain__domain=domain),
            many=True,
            context={"request": request},
        ).data,
    )
