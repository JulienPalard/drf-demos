from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework.response import Response
from habitstracker.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Small viewset to provide users."""

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


def fake_habit(pk, request):
    from random import choice, randint

    habits = [
        "Eat Koreal food",
        "Eat Italian food",
        "Eat Japanese food",
        "Sprot",
        "Drink water",
        "Go to swimming pool",
        "Do upgrades",
        "Do backups",
        "Water plants",
    ]
    return {
        "url": reverse("habits-detail", args=[pk], request=request),
        "name": choice(habits),
        "qty": randint(1, 10),
        "interval": choice(("yearly", "monthly", "weekly", "daily")),
    }


class HabitsViewSet(viewsets.ViewSet):
    """A fake viewset to give fake habits."""

    def list(self, request):
        """Provide Habits."""
        return Response({"items": [fake_habit(pk, request) for pk in range(1, 11)]})

    def retrieve(self, request, pk=None):
        """Provide an Habit."""
        return Response(fake_habit(pk, request))
