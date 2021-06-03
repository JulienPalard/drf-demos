from datetime import timedelta, datetime
import socket
import ssl

import django.contrib.auth.models
from django.db import models
from django.utils import timezone


class User(django.contrib.auth.models.AbstractUser):
    ...


class DomainQuerySet(models.QuerySet):
    def refresh(self):
        limit = timezone.now() - timedelta(minutes=1)
        for domain in Domain.objects.filter(last_check__lt=limit):
            domain.refresh()


def get_server_certificate(addr, port=443, timeout=10):
    """Retrieve the certificate from the server at the specified address."""
    context = ssl.create_default_context()
    with socket.create_connection((addr, port), timeout) as sock:
        with context.wrap_socket(sock, server_hostname=addr) as sslsock:
            return sslsock.getpeercert()


class Domain(models.Model):
    objects = DomainQuerySet.as_manager()
    domain = models.CharField(max_length=512)
    is_up = models.BooleanField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_check = models.DateTimeField(auto_now_add=True)

    def refresh(self):
        print("Refreshing", self.domain)
        deadline = timedelta(days=15)
        now = timezone.now()
        is_up, message = True, None
        try:
            cert = get_server_certificate(self.domain)
        except socket.timeout:
            is_up, message = False, "connect timeout"
        except ConnectionResetError:
            is_up, message = False, "Connection reset"
        except Exception as err:
            is_up, message = False, str(err)
        else:
            not_after = datetime.strptime(
                cert["notAfter"], "%b %d %H:%M:%S %Y GMT"
            ).replace(tzinfo=timezone.utc)
            expire_in = not_after - now
            if expire_in < deadline:
                is_up, message = (
                    False,
                    "TLS certificate expire in "
                    f"{expire_in.total_seconds() // 86400:.0f} days",
                )
        Check.objects.create(domain=self, is_up=is_up, message=message)
        self.is_up = is_up
        self.last_check = now
        self.save()

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
