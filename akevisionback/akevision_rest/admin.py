from django.contrib import admin
from .models import Compagnie, Client, RefreshToken, AccessToken

class CompagnieAdmin(admin.ModelAdmin):
    pass

admin.site.register(Compagnie, CompagnieAdmin)


class CLientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, CLientAdmin)


class RefreshTokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(RefreshToken, RefreshTokenAdmin)


class AccessTokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(AccessToken, AccessTokenAdmin)