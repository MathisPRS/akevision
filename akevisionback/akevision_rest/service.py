from django.conf import settings
from .mailing.email_factory import create_email
import jwt
from akevision import settings
from datetime import datetime, timedelta
from .models import Client

def send_mail_information():
    mail_param_dict = {}
    mail_param_dict['body'] = 'corps du mail'
    # premier paramètre : choix du template de mail
    # deuxième paramètre : données et variables que l'on souhaite utiliser dans le mail
    # troisième paramètre : array avec la liste des mails des destinataires
    mail_to_send = create_email('warning', mail_param_dict, ['prenom.nom@mail.com'])
    mail_to_send.send(fail_silently=False)

class TokenService:
    def generate_token(client_id):
        expiration_time = datetime.utcnow() + timedelta(minutes=30)
        payload = {
            'client_id': client_id,
             'exp': int(expiration_time.timestamp()),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    
    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # vérifier que le token n'a pas expiré
            expiration_time = datetime.utcfromtimestamp(payload['exp'])
            if expiration_time < datetime.utcnow():
                raise Exception('Le token a expiré')
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception('Le token a expiré')
        except jwt.InvalidTokenError:
            raise Exception('Le token est invalide')
        
    # def get_client_token(client_id):
    #     client = Client.objects.get(id=client_id)
    #     print(client.token)
    #     return client.token