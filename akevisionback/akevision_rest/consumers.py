import json, datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from .service import TokenService
from .models import Client, RefreshToken, AccessToken

class ClientWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        url_parts = self.scope['url_route']['kwargs']
        client_id = url_parts['client_id']
        print(client_id)
        print(self.receive)
        print(self.__dict__)
        # Attendre de recevoir des données du client

        data = await self.receive()
        if data is None:
            print('Aucune donnée reçue')
            await self.close()
            return

        try:
            data = json.loads(data)
            access_token = data['token']
        except (TypeError, KeyError) as e:
            print('Données invalides')
            await self.close()
            return

        try:
            payload = TokenService.decode_access_token(access_token)
            if payload['client_id'] != client_id:
                await self.close()
                return

            client = Client.objects.get(id=client_id)

            if client.ipv4 != self.scope['client'][0]:
                await self.close()
                return

            refresh_token = TokenService.generate_refresh_token(client)
            client.refresh_token = refresh_token
            client.save()

            await self.accept()

        except Exception as e:
            print(e)
            await self.close()
            return