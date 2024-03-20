import json, datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from .service import TokenService
from .models import Client, RefreshToken, AccessToken

class ClientWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        url_parts = self.scope['url_route']['kwargs']
        client_id = url_parts['client_id']
        print(client_id)

        token = None
        for header, value in self.scope['headers']:
            if header.decode() == 'authorization':
                token = value.decode()
                break
        print(token)

        if not token:
            print('Jeton d\'authentification manquant')
            await self.close()
            return

        # Vérifier le jeton d'authentification
        try:
            payload = TokenService.decode_access_token(token)
            if payload['client_id'] != client_id:
                print(f"Le jeton n'appartient pas au client {client_id}")
                await self.close()
                return

            client = Client.objects.get(id=client_id)
            print(f"Client {client.name} trouvé en base de données")

            if client.ipv4 != self.scope['client'][0]:
                print(f"L'adresse IP de la requête ({self.scope['client'][0]}) ne correspond pas à l'adresse IP du client ({client.ipv4})")
                await self.close()
                return

            refresh_token = TokenService.generate_refresh_token(client)
            client.refresh_token = refresh_token
            client.save()

            await self.accept()

        except Client.DoesNotExist:
            print(f"Le client {client_id} n'existe pas en base de données")
            await self.close()
            return

        except Exception as e:
            print(e)
            await self.close()
            return
