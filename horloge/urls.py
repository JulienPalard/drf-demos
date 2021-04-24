from datetime import datetime

from django.urls import path

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def give_the_date(request):
    """Get the current datetime."""
    return Response({"datetime": datetime.now().isoformat()})


urlpatterns = [path("", give_the_date)]
