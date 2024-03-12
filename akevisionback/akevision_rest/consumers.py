import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Client

class ClientWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client = await self.get_client()
        if self.client:
            await self.channel_layer.group_add(
                'client_%s' % self.client.id,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.client:
            await self.channel_layer.group_discard(
                'client_%s' % self.client.id,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        # Traitez les données reçues ici, par exemple :
        # self.client.cpu = message.get('cpu')
        # self.client.ram = message.get('ram')
        # self.client.save()

        # Envoyez les mises à jour à tous les clients connectés
        await self.channel_layer.group_send(
            'client_%s' % self.client.id,
            {
                'type': 'send.update',
                'message': message,
            }
        )

    async def send_update(self, event):
        message = event['message']

        # Envoyez les mises à jour au client Angular
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def get_client(self):
        client_id = self.scope['url_route']['kwargs']['client_id']
        try:
            return Client.objects.get(client_id=client_id)
        except Client.DoesNotExist:
            return None