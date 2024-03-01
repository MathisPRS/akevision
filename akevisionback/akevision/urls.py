"""akevision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include


def get_title(title):
    if "-preprod" in admin.site.site_url:
        return u'RECETTE ' + title
    else:
        return title


admin.site.site_url = settings.SITE_URL
admin.site.site_header = get_title("Administration de QUALIMS")
admin.site.index_title = get_title("Administration des tables")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('akevision_rest/', include('akevision_rest.urls'), name='akevision_rest'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
