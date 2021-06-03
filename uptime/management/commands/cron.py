from django.core.management.base import BaseCommand

from uptime.models import Check, Domain


class Command(BaseCommand):
    help = "Check every domain."

    def handle(self, *args, **options):
        Domain.objects.refresh()
