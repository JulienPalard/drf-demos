from django.contrib.auth.models import User
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
        "done": reverse("habits-done-list", args=[pk], request=request),
    }


def fake_done(habit_pk, pk, request):
    from random import randint
    from datetime import datetime, timedelta

    return {
        "url": reverse("habits-done-detail", args=[habit_pk, pk], request=request),
        "at": (datetime.now() - timedelta(seconds=randint(100, 100_000))).isoformat(),
    }


class HabitsViewSet(viewsets.ViewSet):
    """A fake viewset to give fake habits."""

    def list(self, request):
        """Provide Habits."""
        return Response({"items": [fake_habit(pk, request) for pk in range(1, 11)]})

    def retrieve(self, request, pk=None):
        """Provide an Habit."""
        return Response(fake_habit(pk, request))


class DoneViewSet(viewsets.ViewSet):
    """A fake viewset to give fake habits."""

    def list(self, request, habit_pk):
        """Provide Habits."""
        return Response(
            {"items": [fake_done(habit_pk, pk, request) for pk in range(1, 4)]}
        )

    def retrieve(self, request, habit_pk, pk=None):
        """Provide an Habit."""
        return Response(fake_done(habit_pk, pk, request))
