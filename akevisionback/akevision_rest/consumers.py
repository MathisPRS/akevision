from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Poste
from .service import encrypt_message, decrypt_message
from cryptography.fernet import Fernet
import json
from datetime import datetime, timezone

class PosteWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.poste_id = self.scope['url_route']['kwargs']['poste_id']
        for header, value in self.scope['headers']:
            if header.decode() == 'authorization':
                self.token = value
                break

        try:
            poste = await sync_to_async(Poste.objects.get)(id=self.poste_id, token=self.token)
            self.cipher_suite = Fernet(poste.aes_key)
            self.poste = poste
            # Accepter la connexion
            await self.accept()

            print(f'Connection OK avec {poste.name} + {poste.last_communication}')

            await self.validate_connection()

        except Poste.DoesNotExist:
            print('Poste does not exist')
            await self.close()

    async def disconnect(self, close_code):
        print(f'Disconnected poste_id: {self.poste_id}')

    async def receive(self, text_data):
        # Déchiffrer le message reçu
        decrypted_message = decrypt_message(self.cipher_suite, text_data)
        print(decrypted_message)

        if decrypted_message.get('action') == 'send_info':
            # Première connexion : stocker les informations
            self.poste.name = decrypted_message.get('computer_name')
            self.poste.address_mac = decrypted_message.get('mac_address')
            await sync_to_async(self.poste.save)()
            print(f'Informations stockées pour {self.poste.name}')

        elif decrypted_message.get('action') == 'send_mac':
            # Connexion ultérieure : vérifier l'adresse MAC
            if self.poste.address_mac == decrypted_message.get('mac_address'):
                print(f'Adresse MAC vérifiée pour {self.poste.name}')
            else:
                print(f'Adresse MAC incorrecte pour {self.poste.name}')
                await self.close()

        # Montrer qu'on a bien reçu
        self.poste.last_communication = datetime.now(timezone.utc)
        await sync_to_async(self.poste.save)()
        reponse_message = {'action': 'received', 'data': decrypted_message}
        encrypted_response = encrypt_message(self.cipher_suite, reponse_message)
        await self.send(text_data=encrypted_response)

    async def validate_connection(self):
        if not self.poste.last_communication:
            # Première connexion
            encrypted_message = encrypt_message(self.cipher_suite, {'action': 'request_info'})
            await self.send(text_data=encrypted_message)
            print("message action INFO envoyé")
        else:
            # Connexion ultérieure
            encrypted_message = encrypt_message(self.cipher_suite, {'action': 'request_mac'})
            await self.send(text_data=encrypted_message)
            print("message action MAC envoyé")
