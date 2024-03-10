from django.db import models
import random
import string

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

    def __str__(self):
        return self.name