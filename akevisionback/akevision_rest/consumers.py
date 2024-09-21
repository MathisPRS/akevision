from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Poste
from cryptography.fernet import Fernet
import json

class PosteWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.poste_id = self.scope['url_route']['kwargs']['poste_id']
        for header, value in self.scope['headers']:
            if header.decode() == 'authorization':
                self.token = value
                break

        try:
            poste = await sync_to_async(Poste.objects.get)(id=self.poste_id, token=self.token)
            
            await self.accept()
            self.aes_key = poste.aes_key
            
            print( f'aes_key = {self.aes_key}')
            self.cipher_suite = Fernet(self.aes_key)


            print(f'Nous sommes connecté avec {poste.name}')

        except Poste.DoesNotExist:
            print('Poste does not exist')
            await self.close()

    async def disconnect(self, close_code):
        print(f'Disconnected poste_id: {self.poste_id}')

    async def receive(self, text_data):

        await self.send(text_data=f"Message received: {text_data}")

         # Déchiffrer le message reçu
        decrypted_message = self.cipher_suite.decrypt(text_data.encode()).decode()
        message = json.loads(decrypted_message)
        print(message)
