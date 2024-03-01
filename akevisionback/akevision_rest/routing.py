from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/computer/(?P<computer_id>\d+)/$', consumers.ComputerConsumer.as_asgi()),
    # Ajoutez d'autres routes WebSocket au besoin
]