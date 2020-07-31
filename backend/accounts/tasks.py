import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from .models import MobileToken
from time import sleep
from core.settings import TOKEN_EXPIRE_SECS


@shared_task()
def send_mobile_token(token_id):
    mobile_token = MobileToken.objects.get(id=token_id)
    print(mobile_token.token)  # Pendiente implemente twilio
    sleep(TOKEN_EXPIRE_SECS)
    mobile_token.is_expired = True
    mobile_token.save()
    return mobile_token


@shared_task
def expire_token(mobile_token):
    sleep(TOKEN_EXPIRE_SECS)
    mobile_token.is_expired = True
    mobile_token.save()
