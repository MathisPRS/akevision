from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ClientWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        url_parts = self.scope['url_route']['kwargs']
        client_id = int(url_parts['client_id'])