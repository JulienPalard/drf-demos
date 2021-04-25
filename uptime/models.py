from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=512)
    is_up = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.domain


class Check(models.Model):
    is_up = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="checks")
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.domain.domain} is {'up' if self.is_up else 'down'}"
