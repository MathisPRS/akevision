from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string

from django.conf import settings


def get_email_template(kind):
    return get_template('emails/%s.html' % kind)


def create_email(template_prefix, context, recipient_list):
    """
    Dans le fichier configlocal.cfg on trouve les éléments :
        DEFAULT_FROM_EMAIL : email-expediteur@akema.fr
        EMAIL_SUBJECT_PREFIX : Prefix du mail

    Dans le dossier templates on trouve :
        subject : l'objet du mail que l'on concatène avec le subject_prefix
        context : permet d'envoyer des paramètres et des données sous forme d'un dictionnaire jusqu'au template du corps du mail
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    subject_prefix = settings.EMAIL_SUBJECT_PREFIX
    subject = get_template('emails/{0}/{0}-subject.txt'.format(template_prefix))
    plain_content = get_template('emails/{0}/{0}-content.txt'.format(template_prefix))
    html_content = get_template('emails/{0}/{0}-content.html'.format(template_prefix))
    mail = EmailMultiAlternatives(
          subject=subject_prefix + subject.render(context),
          body=plain_content.render(context),
          from_email=from_email,
          to=recipient_list,
        )
    mail.attach_alternative(html_content.render(context), 'text/html')
    return mail
