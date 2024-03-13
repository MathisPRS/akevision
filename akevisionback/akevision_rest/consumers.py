import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .service import TokenService
from .models import Client

class ClientWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # extraire l'ID du client et le token de l'URL de la requête
        client_id = self.scope['url_route']['kwargs']['client_id']
        token = self.scope['url_route']['kwargs']['token']
        # récupérer le client correspondant dans la base de données
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            await self.close()
            return
        # vérifier que le token correspond à celui stocké dans la base de données
        if token != client.token:
            await self.close()
            return
        # décoder le token pour extraire l'adresse IP du client
        try:
            payload = TokenService.decode_token(token)
            client_ip = payload['ipv4']
            # vérifier que l'adresse IP du client correspond à celle dans la base de données
            if client.ipv4 != client_ip:
                await self.close()
                return
            # accepter la connexion
            await self.accept()
        except Exception as e:
            await self.close()
            print(e)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        # traiter les données envoyées par le client
        # ...
        response = {'status': 'ok'}
        await self.send(text_data=json.dumps(response))