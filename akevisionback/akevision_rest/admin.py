from django.contrib import admin
from .models import Compagnie, Poste, Website, GroupeWebsite, Agent

class CompagnieAdmin(admin.ModelAdmin):
    pass
admin.site.register(Compagnie, CompagnieAdmin)


class PosteAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'compagnie_id', 'os', 'last_communication', 'address_mac', 'token', 'aes_key')
    search_fields = ('name', 'user', 'address_mac')
    list_filter = ('os', 'compagnie_id')

admin.site.register(Poste, PosteAdmin)


class WebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Website, WebsiteAdmin)


class GroupeWebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(GroupeWebsite, GroupeWebsiteAdmin)


class AgentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Agent, AgentAdmin)