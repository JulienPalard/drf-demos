from django.conf import settings
from pathlib import Path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from file.serializers import FileSerializer


@api_view(["GET"])
def file_view(request, file="."):
    """Get file info."""
    file = (Path(settings.ROOT) / file).resolve()
    serializer = FileSerializer(file, context={"request": request})
    return Response(serializer.data)
