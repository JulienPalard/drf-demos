from django.conf import settings
from pathlib import Path
from datetime import date
from rest_framework import serializers
from rest_framework.reverse import reverse


class FileSerializer(serializers.BaseSerializer):
    def to_representation(self, instance: Path):
        stats = instance.stat()
        path = str(instance.resolve().relative_to(settings.ROOT))
        representation = {
            "self": reverse("file", args=(path,), request=self.context["request"]),
            "name": instance.name,
            "path": path,
            "size": stats.st_size,
            "ctime": date.fromtimestamp(stats.st_ctime).isoformat(),
            "mtime": date.fromtimestamp(stats.st_mtime).isoformat(),
            "atime": date.fromtimestamp(stats.st_atime).isoformat(),
            "mode": oct(stats.st_mode),
            "is_dir": bool(stats.st_mode & 0o40000),
        }
        if self.context.get("depth", 1) == 1:
            if representation["is_dir"]:
                representation["files"] = [
                    FileSerializer(
                        file,
                        context={
                            **self.context,
                            "depth": self.context.get("depth", 1) + 1,
                        },
                    ).data
                    for file in instance.glob("*")
                ]
            else:
                try:
                    representation["text"] = instance.read_text()
                except:
                    representation["bytes"] = instance.read_bytes()
        return representation
