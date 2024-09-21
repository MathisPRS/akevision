from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/poste/(?P<poste_id>[^/.]+)/$', consumers.PosteWebsocketConsumer.as_asgi()),
]
