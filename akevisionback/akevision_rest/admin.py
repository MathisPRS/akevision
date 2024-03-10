from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import Compagnie
from .models import Client

class CompagnieAdmin(admin.ModelAdmin):
    pass

admin.site.register(Compagnie, CompagnieAdmin)

class CLientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, CLientAdmin)

