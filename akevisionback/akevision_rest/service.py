from django.conf import settings
from .mailing.email_factory import create_email
import jwt, uuid
from jose import jwt as jose_jwt
from akevision import settings
from datetime import datetime, timedelta, timezone
from .models import RefreshToken, AccessToken, Client

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
        expiration_time = datetime.now() + timedelta(days=1)
        payload = {
            'client_id': client.id,
            'exp': int(expiration_time.timestamp()),
        }
        
        access_token= AccessToken.objects.create(
            access_token= jose_jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256'),
            created_at=datetime.now(),
            expired=False,
            client_acces_token = client,
        )
        return access_token
    
    @staticmethod
    def decode_access_token(access_token):
        try:
            payload = jose_jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            client_id = payload.get('client_id')
            expiration_time = datetime.fromtimestamp(payload.get('exp'))
            if datetime.now() > expiration_time:
                raise Exception('Access token expired')
            return client_id
        except Exception as e:
            raise Exception('Invalid access token')

    
    @staticmethod
    def generate_refresh_token(client):
        refresh_token = uuid.uuid4().hex
        RefreshToken.objects.create(token=refresh_token, client=client)
        return refresh_token

    @staticmethod
    def validate_access_token(access_token):
        try:
            payload = jose_jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            # Vérifier que le token n'a pas expiré
            expiration_time = datetime.fromtimestamp(payload['exp'])
            if expiration_time < datetime.now():
                raise Exception('Le token a expiré')
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception('Le token a expiré')
        except jwt.InvalidTokenError:
            raise Exception('Le token est invalide')

    @staticmethod
    def validate_refresh_token(refresh_token):
        try:
            refresh_token_obj = RefreshToken.objects.get(token=refresh_token, expired=False)
            return refresh_token_obj.client
        except RefreshToken.DoesNotExist:
            raise Exception('Le jeton de rafraîchissement est invalide ou a expiré')
        
    @staticmethod
    def get_client_from_access_token(access_token):
        try:
            token = AccessToken.objects.get(access_token=access_token, expired=False)
            if token.created_at < timezone.now() - timedelta(days=1):
                token.expired = True
                token.save()
                raise jwt.InvalidTokenError('Access token expiré')
            return token.client_acces_token
        except AccessToken.DoesNotExist:
            raise jwt.InvalidTokenError('Access token invalide')
