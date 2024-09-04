from celery import shared_task
import ssl
import socket
from datetime import datetime
import pytz
from .models import Website

@shared_task
def update_ssl_expiration():
    websites = Website.objects.all()
    for website in websites:
        url = website.url.replace('https://', '')
        try:
            context = ssl.create_default_context()
            with context.wrap_socket(socket.create_connection((url, 443)), server_hostname=url) as s:
                cert = s.getpeercert()
            subject = dict(x[0] for x in cert['subject'])
            issued_date = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=pytz.UTC)
            expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=pytz.UTC)
            ssl_expiration = (expire_date - datetime.now(pytz.UTC)).days
            website.ssl_expiration = ssl_expiration
            website.save()
        except Exception as e:
            print(f"Error updating SSL expiration for {url}: {e}")
