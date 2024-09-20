import io
import zipfile
from django.conf import settings
from .mailing.email_factory import create_email
import os, jwt, json
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
