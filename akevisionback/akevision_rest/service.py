from django.conf import settings
from .mailing.email_factory import create_email
import jwt, uuid
from jose import jwt as jose_jwt
from akevision import settings
from datetime import datetime, timedelta, timezone
from .models import RefreshToken, AccessToken, Client
from django.utils.timezone import make_aware

def send_mail_information():
    mail_param_dict = {}
    mail_param_dict['body'] = 'corps du mail'
    # premier paramètre : choix du template de mail
    # deuxième paramètre : données et variables que l'on souhaite utiliser dans le mail
    # troisième paramètre : array avec la liste des mails des destinataires
    mail_to_send = create_email('warning', mail_param_dict, ['prenom.nom@mail.com'])
    mail_to_send.send(fail_silently=False)

class TokenService:
    @staticmethod
    def generate_access_token(client):
        payload = {
            'client_id': client.id,
            'ip_address': client.ipv4,
        }
        
        access_token= AccessToken.objects.create(
            access_token= jose_jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256'),
            created_at=datetime.now(),
            expired=False,
            client_acces_token = client,
        )
        return access_token
    
    @staticmethod
    def decode_access_token(token):
        try:
            # Décoder le jeton avec la clé secrète
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception('Le jeton a expiré')
        except jwt.DecodeError:
            raise Exception('Signature invalide')
    

    @staticmethod
    def get_access_token(token):
        try:
            # vérification que le token existe en base
            access_token = AccessToken.objects.get(access_token=token, expired=False)
            print('get_access_token' , access_token.created_at )

            #created_at_aware = make_aware(access_token.created_at)

            # vérification que le token ne soit pas exipré
            if access_token.created_at < datetime.now(timezone.utc) - timedelta(days=5):
                access_token.expired = True
                access_token.save()
                raise jwt.InvalidTokenError('Access token expiré')
            return access_token
        except AccessToken.DoesNotExist:
            raise Exception('Le jeton n\'existe pas dans la base de données')
        
    
    @staticmethod
    def is_token_linked_to_client(token, client_id):
        try:
            client = Client.objects.get(id=client_id)
            access_token = AccessToken.objects.get(client_acces_token=client)
            if token != access_token :
                raise Exception('Le Token n\'est pas lié avec le bon client')
            return access_token
                
        except AccessToken.DoesNotExist:
            raise Exception('Il n\'existe pas de token dans la base pour le client demandé')
        except Client.DoesNotExist:
             raise Exception('Le client n\'existe pas')

        
    @staticmethod
    def validate_access_token(token, url_client, ip_address):
        try:
            # Vérifier que le token n'a pas expiré
            payload = TokenService.decode_access_token(token)
            print('validate_access_token ', payload)
            client_id = payload['client_id']

            print('validate_access_token ', client_id)
            client = Client.objects.get(id=client_id) 

            # Vérifier que l'id pu payload egale a celui de l'url
            if client_id != url_client :
                raise Exception('L\'id client du payload et de l\'url sont différent')
            
            # Vérifier que le token est bon
            acces_token = TokenService.get_access_token(token)
            print('validate_access_token ', acces_token)
            TokenService.is_token_linked_to_client(acces_token, client_id)

              

            # Vérifier que l'IP de la base client egale a celui de l'url
            print('validate_access_token ', client.ipv4)
            print('validate_access_token ', ip_address)
            if client.ipv4  != ip_address :
                raise Exception('L\'adresse IP du payload et de la requête sont différentes')
            
        except jwt.InvalidTokenError:
            raise Exception('Le token est invalide')