from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


@shared_task
def send_email_confirm(current_site_domain, new_user_pk, to_email):
    new_user = get_user_model().objects.get(pk=new_user_pk)
    mail_subject = 'Activation link has been sent to your email id'
    message = render_to_string('registration/acc_active_email.html', {
        'user': new_user,
        'domain': current_site_domain,
        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
        'token': account_activation_token.make_token(new_user),
    })
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    return email.send()
