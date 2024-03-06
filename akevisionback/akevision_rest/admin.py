from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import Compagnie

class CompagnieAdmin(admin.ModelAdmin):
    pass

admin.site.register(Compagnie, CompagnieAdmin)
