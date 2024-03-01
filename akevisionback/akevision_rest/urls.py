from django.urls import path
from rest_framework import routers

from channels.routing import ProtocolTypeRouter
from . import consumers
from .auth_views import AuthAPIView
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'manage-file', views.ManageFileViewSet, basename='manage-file')
router.register(r'mail', views.MailViewset, basename='mail')

urlpatterns = [
    path("auth/", AuthAPIView.as_view(), name='test'),
]

urlpatterns += router.urls
