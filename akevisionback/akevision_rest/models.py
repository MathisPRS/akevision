from django.db import models

class Compagnie(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Poste(models.Model):
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255,null=True, blank=True)
    compagnie_id = models.ForeignKey(Compagnie, on_delete=models.CASCADE,null=True, blank=True )
    OS_CHOICES = [
        ('Linux', 'Linux'),
        ('Windows', 'Windows'),
    ]
    os = models.CharField(max_length=10, choices=OS_CHOICES, null=True, blank=True)
    last_communication = models.DateTimeField(null=True, blank=True)
    address_mac = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    aes_key = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('address_mac', 'compagnie_id')

    def __str__(self):
        return self.name
  
 
class GroupeWebsite(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Website(models.Model):
    nameWebsite = models.CharField(max_length=255)
    groupe = models.ForeignKey(GroupeWebsite, on_delete=models.CASCADE,null=True, blank=True )
    url = models.CharField(max_length=255,null=True, blank=True)
    ALERTE_CHOICES = [
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ]
    alerte = models.CharField(max_length=10, choices=ALERTE_CHOICES, null=True, blank=True)
    ssl_expiration = models.IntegerField(null=True)
    COULEUR_CHOICES = [
        ('rouge', 'Rouge'),
        ('orange', 'Orange'),
        ('vert', 'Vert'),
        ('gris', 'Gris'),
    ]
    couleur = models.CharField(max_length=10, choices=COULEUR_CHOICES, null=True, blank=True)
    last_verification = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ('nameWebsite', 'groupe')

    def __str__(self):
        return self.nameWebsite
