from django.contrib import admin
from .models import Compagnie, Poste, Website, GroupeWebsite

class CompagnieAdmin(admin.ModelAdmin):
    pass
admin.site.register(Compagnie, CompagnieAdmin)


class PosteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Poste, PosteAdmin)


class WebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Website, WebsiteAdmin)


class GroupeWebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(GroupeWebsite, GroupeWebsiteAdmin)