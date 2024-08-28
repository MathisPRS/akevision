from django.contrib import admin
from .models import Compagnie, Client, RefreshToken, AccessToken, Website, GroupeWebsite

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


class WebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Website, WebsiteAdmin)


class GroupeWebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(GroupeWebsite, GroupeWebsiteAdmin)