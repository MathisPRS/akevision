from django.conf import settings
from .mailing.email_factory import create_email
import jwt, uuid
from jose import jwt as jose_jwt
from akevision import settings
from datetime import datetime, timedelta
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
        expiration_time = datetime.utcnow() + timedelta(minutes=30)
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
    def generate_refresh_token(client):
        refresh_token = uuid.uuid4().hex
        RefreshToken.objects.create(token=refresh_token, client=client)
        return refresh_token

    @staticmethod
    def validate_access_token(access_token):
        try:
            payload = jose_jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            # Vérifier que le token n'a pas expiré
            expiration_time = datetime.utcfromtimestamp(payload['exp'])
            if expiration_time < datetime.utcnow():
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
