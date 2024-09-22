import io
import zipfile
from django.conf import settings
from .mailing.email_factory import create_email
import os, jwt, json
from cryptography.fernet import Fernet
from jose import jwt as jose_jwt
from akevision import settings
from datetime import datetime, timedelta, timezone
from .models import Poste
from django.utils.timezone import make_aware
from django.conf import settings

def send_mail_information():
    mail_param_dict = {}
    mail_param_dict['body'] = 'corps du mail'
    # premier paramètre : choix du template de mail
    # deuxième paramètre : données et variables que l'on souhaite utiliser dans le mail
    # troisième paramètre : array avec la liste des mails des destinataires
    mail_to_send = create_email('warning', mail_param_dict, ['prenom.nom@mail.com'])
    mail_to_send.send(fail_silently=False)

def generate_token(compagnie_id, compagnie_name):
    payload = {
        'compagnie_id': compagnie_id,
        'compagnie_name': compagnie_name,
        
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def generate_aes_key():
    key = Fernet.generate_key()
    return key

def encrypt_message(cipher_suite, message):
    encrypted_message = cipher_suite.encrypt(json.dumps(message).encode())
    return encrypted_message.decode()

def decrypt_message(cipher_suite, encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode()).decode()
    return json.loads(decrypted_message)