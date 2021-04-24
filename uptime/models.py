from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=512)
    is_up = models.BooleanField(null=True, blank=True)


class Check(models.Model):
    is_up = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="checks")
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]
