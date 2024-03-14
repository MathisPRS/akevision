# import json, datetime
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .service import TokenService
# from .models import Client, RefreshToken, AccessToken

# class ClientWebsocketConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # extraire l'ID du client et le jeton d'accès de l'URL de la requête
#         client_id = self.scope['url_route']['kwargs']['client_id']
#         access_token = self.scope['url_route']['kwargs']['access_token']

#         try:
#             # Vérifier que le jeton d'accès est valide
#             payload = TokenService.validate_access_token(access_token)

#             # Récupérer le client correspondant dans la base de données
#             client = Client.objects.get(id=client_id)

#             # Vérifier que le jeton d'accès correspond à celui stocké dans la base de données
#             token_obj = Token.objects.get(token=access_token)
#             if token_obj.expired:
#                 raise Exception('Le jeton d\'accès a expiré')
#             if datetime.datetime.utcfromtimestamp(payload['exp']) < datetime.datetime.utcnow():
#                 token_obj.expired = True
#                 token_obj.save()
#                 raise Exception('Le jeton d\'accès a expiré')
#             if payload['client_id'] != client.id:
#                 await self.close()
#                 return

#             # Vérifier que l'adresse IP du client correspond à celle stockée dans la base de données
#             if client.ipv4 != self.scope['client'][0]:
#                 await self.close()
#                 return

#             # Accepter la connexion
#             await self.accept()
#         except Exception as e:
#             await self.close()
#             print(e)

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         if data.get('type') == 'renew_token':
#             refresh_token = data.get('refresh_token')
#             if not refresh_token:
#                 await self.send_error('Aucun jeton de rafraîchissement fourni')
#                 return
#             try:
#                 await self.renew_token(refresh_token)
#             except Exception as e:
#                 await self.send_error(str(e))
#                 return
#         else:
#             # traiter les données envoyées par le client
#             # ...
#             response = {'status': 'ok'}
#             await self.send(text_data=json.dumps(response))

#     async def renew_token(self, refresh_token):
#         try:
#             # Vérifier que le jeton de rafraîchissement est valide
#             client_id = TokenService.validate_refresh_token(refresh_token)
#             client = Client.objects.get(id=client_id)

#             # Générer un nouveau jeton d'accès et un nouveau jeton de rafraîchissement
#             access_token = TokenService.generate_access_token(client)
#             refresh_token = TokenService.generate_refresh_token(client)

#             # Mettre à jour le jeton d'accès et le jeton de rafraîchissement du client
#             client.token = access_token
#             client.refresh_token = refresh_token
#             client.save()

#             # Renvooyer le nouveau jeton d'accès au client
#             await self.send(text_data=json.dumps({
#                 'type': 'new_access_token',
#                 'access_token': access_token
#             }))
#         except Exception as e:
#             await self.send_error(str(e))


#     async def send_error(self, message):
#         await self.send(text_data=json.dumps({
#             'type': 'error',
#             'message': message
#         }))
