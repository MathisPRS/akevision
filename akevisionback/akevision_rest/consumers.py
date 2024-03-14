import json, datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from .service import TokenService
from .models import Client, RefreshToken, AccessToken

class ClientWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        url_parts = self.scope['url_route']['kwargs']
        client_id = url_parts['client_id']
        access_token = url_parts['token']

        try:
            payload = TokenService.decode_access_token(access_token)

            # Vérifier que l'access token est attribué avec le bon ID client
            if payload['client_id'] != client_id:
                await self.close()
                return

            client = Client.objects.get(id=client_id)

            # Vérifier que l'adresse IP du client correspond à celle stockée dans la table client
            if client.ipv4 != self.scope['client'][0]:
                await self.close()
                return

            # Créer un nouveau refresh token pour le client
            refresh_token = TokenService.generate_refresh_token(client)
            client.refresh_token = refresh_token
            client.save()

            # Accepter la connexion WebSocket
            await self.accept()

        except Exception as e:
            print(e)
            await self.close()
            return


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'renew_token':
            refresh_token = data.get('refresh_token')
            if not refresh_token:
                await self.send_error('Aucun jeton de rafraîchissement fourni')
                return
            try:
                await self.renew_token(refresh_token)
            except Exception as e:
                await self.send_error(str(e))
                return
        else:
            # traiter les données envoyées par le client
            # ...
            response = {'status': 'ok'}
            await self.send(text_data=json.dumps(response))

    async def renew_token(self, refresh_token):
        try:
            # Vérifier que le jeton de rafraîchissement est valide
            client_id = TokenService.validate_refresh_token(refresh_token)
            client = Client.objects.get(id=client_id)

            # Générer un nouveau jeton d'accès et un nouveau jeton de rafraîchissement
            access_token = TokenService.generate_access_token(client)
            refresh_token = TokenService.generate_refresh_token(client)

            # Mettre à jour le jeton d'accès et le jeton de rafraîchissement du client
            client.token = access_token
            client.refresh_token = refresh_token
            client.save()

            # Renvooyer le nouveau jeton d'accès au client
            await self.send(text_data=json.dumps({
                'type': 'new_access_token',
                'access_token': access_token
            }))
        except Exception as e:
            await self.send_error(str(e))


    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))
