from celery import shared_task
import ssl
import socket
from datetime import datetime, timedelta
import pytz
from .models import Website
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_ssl_expiration():
    websites = Website.objects.all()
    today = datetime.now(pytz.UTC).date()

    for website in websites:
        url = website.url.replace('https://', '')

        # Vérifier si last_verification est null ou date de plus d'un jour
        if not website.last_verification or website.last_verification < today:
            try:
                context = ssl.create_default_context()
                with context.wrap_socket(socket.create_connection((url, 443)), server_hostname=url) as s:
                    cert = s.getpeercert()
                subject = dict(x[0] for x in cert['subject'])
                issued_date = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=pytz.UTC)
                expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=pytz.UTC)
                ssl_expiration = (expire_date - datetime.now(pytz.UTC)).days
                logger.info(f"{website} {url} {ssl_expiration}")
                website.ssl_expiration = ssl_expiration

                # Attribuer une couleur en fonction de la valeur de ssl_expiration
                if ssl_expiration is None:
                    website.couleur = 'gris'
                elif ssl_expiration <= 5:
                    website.couleur = 'rouge'
                elif ssl_expiration <= 30:
                    website.couleur = 'orange'
                else:
                    website.couleur = 'vert'

                website.last_verification = today
                website.save()
                logger.info(f"Updated {website} with last_verification: {today}")
            except Exception as e:
                logger.error(f"Error updating SSL expiration for {url}: {e}")
