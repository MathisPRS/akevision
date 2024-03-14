# import datetime, jwt
# from django.utils.deprecation import MiddlewareMixin
# from channels.db import database_sync_to_async
# from akevision_rest.models import Client, Token
# from akevision_rest.service import TokenService

# class TokenExpirationMiddleware:
#     def __init__(self, app):
#         self.app = app

#     async def __call__(self, scope, receive, send):
#         # Vérifier si la requête contient un jeton d'accès dans l'URL
#         access_token = scope['query_string'].decode().split('=')[-1]
#         if access_token:
#             try:
#                 # Valider le jeton d'accès et récupérer l'ID du client
#                 payload = await database_sync_to_async(TokenService.validate_access_token)(access_token)
#                 client_id = payload['client_id']
#                 token_obj = await database_sync_to_async(Token.objects.get)(token=access_token)
#                 if token_obj.expired:
#                     raise Exception('Le jeton d\'accès a expiré')
#                 if datetime.datetime.utcfromtimestamp(payload['exp']) < datetime.datetime.utcnow():
#                     token_obj.expired = True
#                     await database_sync_to_async(token_obj.save)()
#                     raise Exception('Le jeton d\'accès a expiré')
#                 client = await database_sync_to_async(Client.objects.get)(id=client_id)

#                 # Ajouter l'ID du client à la portée de la connexion WebSocket
#                 scope['client_id'] = client_id

#                 # Appeler le middleware suivant
#                 return await self.app(scope, receive, send)

#             except Exception as e:
#                 print(e)
#                 # Fermer la connexion WebSocket avec le code 1008 ("Policy Violation")
#                 await send({
#                     'type': 'websocket.close',
#                     'code': 1008,
#                 })
#         else:
#             # Fermer la connexion WebSocket avec le code 1002 ("Protocol Error")
#             await send({
#                 'type': 'websocket.close',
#                 'code': 1002,
#             })
