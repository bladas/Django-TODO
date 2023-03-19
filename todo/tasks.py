from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(serializer='json', name="send_mail")
def send_email(subject, message, receivers):
    send_mail(subject, message, settings.EMAIL_HOST_USER, receivers)
