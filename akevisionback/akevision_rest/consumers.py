from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .service import TokenService
from .models import Client, RefreshToken, AccessToken

class ClientWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        url_parts = self.scope['url_route']['kwargs']
        client_id = int(url_parts['client_id'])

        token = None
        for header, value in self.scope['headers']:
            if header.decode() == 'authorization':
                token = value.decode()
                break

        if not token:
            print('Jeton d\'authentification manquant')
            await self.close()
            return

        validate_access_token_async = sync_to_async(TokenService.validate_access_token)

        # Vérifier le jeton d'authentification
        try:
            await validate_access_token_async(token, client_id, self.scope['client'][0])
            await self.accept()

        except Client.DoesNotExist:
            print(f"Le client {client_id} n'existe pas en base de données")
            await self.close()
            return

        except Exception as e:
            print(e)
            await self.close()
            return
