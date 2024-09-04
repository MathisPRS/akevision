import ssl
import socket
from datetime import datetime
import pytz

def update_ssl_expiration():
    websites = {
        'akema': 'akema.fr',
        'apidae': 'apidae.biz',
        'google': 'google.com'
    }
    for name, url in websites.items():
        # Remove the https:// prefix from the URL
        url = url.replace('https://', '')
        try:
            context = ssl.create_default_context()
            with context.wrap_socket(socket.create_connection((url, 443)), server_hostname=url) as s:
                cert = s.getpeercert()
            subject = dict(x[0] for x in cert['subject'])
            issued_date = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=pytz.UTC)
            expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=pytz.UTC)
            ssl_expiration = (expire_date - datetime.now(pytz.UTC)).days
            print(f"{name}:")
            print(f"Common Name: {subject.get('commonName', '')}")
            print(f"Organization: {subject.get('organizationName', '')}")
            print(f"Organizational Unit: {subject.get('organizationalUnitName', '')}")
            print(f"Issued Date: {issued_date}")
            print(f"Expiration Date: {expire_date}")
            print(f"SSL Expiration: {ssl_expiration} days")
        except Exception as e:
            print(f"Error updating SSL expiration for {url}: {e}")

if __name__ == '__main__':
    update_ssl_expiration()