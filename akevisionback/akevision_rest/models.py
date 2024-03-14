from django.db import models

class Compagnie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=255)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE,null=True, blank=True )
    OS_CHOICES = [
        ('Linux', 'Linux'),
        ('Windows', 'Windows'),
    ]
    os = models.CharField(max_length=10, choices=OS_CHOICES, null=True, blank=True)
    ipv4 = models.CharField(max_length=255,null=True, blank=True)
    
    class Meta:
        unique_together = ('name', 'compagnie')

    def __str__(self):
        return self.name


class AccessToken(models.Model):
    access_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)
    client_acces_token = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name='client_refresh_token')
    
    def __str__(self):
        return self.access_token
    

class RefreshToken(models.Model):
    refresh_token = models.CharField(max_length=255, unique=True)
    expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    client_refresh_token = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name='client_access_token')


    def __str__(self):
        return self.refresh_token