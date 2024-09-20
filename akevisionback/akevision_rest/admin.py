from django.contrib import admin
from .models import Compagnie, Client, Website, GroupeWebsite

class CompagnieAdmin(admin.ModelAdmin):
    pass
admin.site.register(Compagnie, CompagnieAdmin)


class CLientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, CLientAdmin)


class WebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Website, WebsiteAdmin)


class GroupeWebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(GroupeWebsite, GroupeWebsiteAdmin)