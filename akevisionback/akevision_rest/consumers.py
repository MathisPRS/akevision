from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Poste, Compagnie
from .service import encrypt_message, decrypt_message
from cryptography.fernet import Fernet
import json, zoneinfo
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

            print(f'Connection OK avec {poste.name}')

            await self.validate_connection()

        except Poste.DoesNotExist:
            print('Poste does not exist')
            await self.close()

    async def disconnect(self, close_code):
        self.poste.is_connected = False
        self.poste.cpu_usage = None
        self.poste.ram_usage = None
        await sync_to_async(self.poste.save)()
        print(f'Disconnected poste_id: {self.poste_id}')

    async def receive(self, text_data):
        # Déchiffrer le message reçu
        decrypted_message = decrypt_message(self.cipher_suite, text_data)
        action = decrypted_message.get('action')
        handlers = {
            'send_token': self.handle_send_token,
            'get_info': self.handle_get_info,
        }

        handler = handlers.get(action)
        if handler:
            await handler(decrypted_message)
        else:
            print(f'Action inconnue: {action}')

    async def handle_send_token(self, message):
        # Vérifier le token de la compagnie
        # compagnie_token = message.get('compagnie_token')
        # compagnie = await sync_to_async(Compagnie.objects.get)(id=self.poste.compagnie_id.id)
        # if compagnie.token == compagnie_token:
        self.poste.address_mac = message.get('mac_address')
        await sync_to_async(self.poste.save)()
        print(f'Token de la compagnie vérifié pour {self.poste.name}')
        # else:
        #     print(f'Token de la compagnie incorrect pour {self.poste.name}')
        #     await self.close()

    async def handle_get_info(self, message):
        date_now = datetime.now(timezone.utc).astimezone(zoneinfo.ZoneInfo("Europe/Paris"))
        print(date_now)
        # Vérifier l'adresse MAC avant d'accepter les informations
        if self.poste.address_mac == message.get('mac_address'):
            self.poste.name = message.get('computer_name')
            self.poste.user = message.get('full_username')
            self.poste.address_mac = message.get('mac_address')
            self.poste.last_communication = date_now
            self.poste.cpu_usage = message.get('cpu_usage')
            self.poste.ram_usage = message.get('ram_usage')
            self.poste.is_connected = True
            await sync_to_async(self.poste.save)()
            print(f'Informations stockées pour {self.poste.name}')

            # Montrer qu'on a bien reçu
            reponse_message = {'action': 'received', 'data': message}
            encrypted_response = encrypt_message(self.cipher_suite, reponse_message)
            await self.send(text_data=encrypted_response)
        else:
            print(f'Adresse MAC incorrecte pour {self.poste.name}')
            await self.close()

    async def validate_connection(self):
        if not self.poste.last_communication:
            # Première connexion
            encrypted_message = encrypt_message(self.cipher_suite, {'action': 'request_token'})
            await self.send(text_data=encrypted_message)
            print("message action TOKEN envoyé")
        else:
            # Connexion ultérieure
            encrypted_message = encrypt_message(self.cipher_suite, {'action': 'request_info'})
            await self.send(text_data=encrypted_message)
            print("message action INFO envoyé")
