from django.conf import settings
from .mailing.email_factory import create_email


def send_mail_information():
    mail_param_dict = {}
    mail_param_dict['body'] = 'corps du mail'
    # premier paramètre : choix du template de mail
    # deuxième paramètre : données et variables que l'on souhaite utiliser dans le mail
    # troisième paramètre : array avec la liste des mails des destinataires
    mail_to_send = create_email('warning', mail_param_dict, ['prenom.nom@mail.com'])
    mail_to_send.send(fail_silently=False)
