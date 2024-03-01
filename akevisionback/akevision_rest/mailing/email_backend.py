from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend
from .akevision import settings


class EmailBackend(DjangoEmailBackend):
    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        self.host = settings.email['host']
        self.port = settings.email['port']
        self.username = settings.email['username']
        self.password = settings.email['password']
        self.use_tls = settings.email['use_tls']
        self.use_ssl = settings.email['use_ssl']
