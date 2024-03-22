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
        ipv4_requete = self.scope['client'][0]
        # Vérifier le jeton d'authentification
        try:
            await validate_access_token_async(token, client_id, ipv4_requete)
            await self.accept()

        except Exception as e:
            print(e)
            await self.close()
            return
