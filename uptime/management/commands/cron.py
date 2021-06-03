from datetime import timedelta, datetime
import socket
import ssl

from django.core.management.base import BaseCommand
from uptime.models import Domain, Check


def get_server_certificate(addr, port=443, timeout=10):
    """Retrieve the certificate from the server at the specified address" """
    context = ssl.create_default_context()
    with socket.create_connection((addr, port), timeout) as sock:
        with context.wrap_socket(sock, server_hostname=addr) as sslsock:
            return sslsock.getpeercert()


class Command(BaseCommand):
    help = "Check every domain."

    def handle(self, *args, **options):
        deadline = timedelta(days=15)
        now = datetime.now()
        is_up, message = True, None
        for domain in Domain.objects.all():
            try:
                cert = get_server_certificate(domain.domain)
            except socket.timeout:
                is_up, message = False, "connect timeout"
            except ConnectionResetError:
                is_up, message = False, "Connection reset"
            except Exception as err:
                is_up, message = False, str(err)
            else:
                not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y GMT")
                expire_in = not_after - now
                if expire_in < deadline:
                    is_up, message = (
                        False,
                        "TLS certificate expire in "
                        f"{expire_in.total_seconds() // 86400:.0f} days",
                    )
            Check.objects.create(domain=domain, is_up=is_up, message=message)
            domain.is_up = is_up
            domain.save()
